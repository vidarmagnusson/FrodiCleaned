# -*- encoding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from django.utils.translation import ugettext as _

from creativecommons.models import License
from schools.models.schools import School
from country.models.regions import Municipality
from structure.utils import slugicefy

import lxml.html
import urllib
import urlparse

from hashlib import md5
from datetime import datetime

import uuid

class ActivityConstruct(models.Model):
	atom_id = models.CharField(max_length=256, editable=False)
	title = models.CharField(max_length=140)

	creator = models.ForeignKey('Person', null=True, editable=False)
	permalink = models.URLField(editable=False)

	updated = models.DateTimeField(auto_now=True)
	published = models.DateTimeField(editable=False, default=datetime.now)

	def __unicode__(self):
		return self.title

	def ostatus(self):
		return {'title':self.title,
			'id':self.atom_id,
			'objecttype':'general contruct',
			'author':self.creator,
			'permalink':self.permalink,
			'last update':self.updated,
			'published':self.published}

	def title_link(self):
		return '<a href="%s">%s</a>' % (self.permalink, self.title)

	def save(self, *args, **kwargs):
       		if self.atom_id == "":
       			self.atom_id = str(uuid.uuid1())
			self.permalink = reverse('view-entry', kwargs={'entry':self.atom_id})
			# Get target if there is any
			target_atom = kwargs.pop('target', None)
			if target_atom:
				try:
					target = ActivityConstruct.objects.get(atom_id=target_atom)
				except:
					target = None
			else:
				target = None
			super(ActivityConstruct, self).save(*args, **kwargs)
			if self.creator:
				self.creator.post(self, target=target)
		else:
			super(ActivityConstruct, self).save(*args, **kwargs)
			if self.creator:
				self.creator.update(self)


class ActivityEntry(models.Model):
	atom_id = models.CharField(max_length=256, editable=False)
	actor = models.ForeignKey('Person', related_name='person_activity')
	activityobject = models.ForeignKey('ActivityConstruct', related_name='object_activity')
	target = models.ForeignKey('ActivityConstruct', blank=True, null=True, related_name='target_activity')
	verb = models.CharField(max_length=128)
	time = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=256)
	summary = models.TextField()
	permalink = models.URLField()

	def __unicode__(self):
		return self.title

	def set_title_summary(self, text):
		self.title = text % (self.actor, self.activityobject)
		self.summary = text % (self.actor.title_link(), self.activityobject.title_link())
		if self.target:
			self.title += ' in %s' % (self.target)
			self.summary += ' in %s' % (self.target.title_link())

	def save(self, *args, **kwargs):
		self.atom_id = str(uuid.uuid1())
		self.permalink = reverse('view-entry', kwargs={'entry':self.atom_id})
		super(ActivityEntry, self).save()



def create_userprofile(sender, instance, signal, *args, **kwargs):
        try:
                profile = Person.objects.get(user=instance)
        except:
                hashed_email = md5(instance.email.strip().lower()).hexdigest()
                person = Person.objects.create(user=instance, title=instance.username,avatar='http://www.gravatar.com/avatar/'+hashed_email, full_name=instance.username)
                person.save()

class Person(ActivityConstruct):
	user = models.ForeignKey(User, unique=True)

	avatar = models.URLField()
	full_name = models.CharField(max_length=128, blank=True, null=True,)
	website = models.URLField(blank=True, null=True)

	school = models.ManyToManyField(School, max_length=128, blank=True, null=True)
	position = models.CharField(max_length=64, blank=True, null=True)


	flattr_uid = models.CharField(max_length=64, null=True, blank=True)
	default_cc_license = models.ForeignKey(License, default=2)

	location = models.ForeignKey(Municipality, blank=True, null=True)

	year_of_birth = models.PositiveIntegerField(blank=True, null=True)
	interests = models.TextField(blank=True, null=True)

	bio = models.TextField(blank=True, null=True)

	# Activities
	following = models.ManyToManyField(ActivityConstruct, related_name='following_set', blank=True, null=True)
	followers = models.ManyToManyField('Person', related_name='followers_set', blank=True, null=True)

	# Used to store "likes" since we don't use favorites
	favorites = models.ManyToManyField(ActivityConstruct, related_name='favorites_set', blank=True, null=True)

	friends = models.ManyToManyField('Person', related_name='friends_set', blank=True, null=True)
	groups = models.ManyToManyField('Group', related_name='members', blank=True, null=True)
	saved_objects = models.ManyToManyField(ActivityConstruct, related_name='saved_objects_set', blank=True, null=True)

	def __unicode__(self):
		return self.user.username

	def latest_note(self):
		try:
			return self.note_set.all().order_by('-published')[0]
		except:
			return 'Þú hefur ekki sagt neitt ennþá :('

	"""
	Finds all the users that this particular user is following and returns
	their user profiles in a list
	"""
	def find_following(self):
		activity_constructs = [a.id for a in self.following.all()]
		return Person.objects.filter(id__in=activity_constructs)

	def count_notes(self):
		return len(Note.objects.filter(creator=self))

	def count_articles(self):
		return len(self.article_set.all())

	def count_photos(self):
		return len(Photo.objects.filter(creator=self))

	def count_videos(self):
		return len(self.video_set.all())

	def count_audio(self):
		return len(self.audio_set.all())

	def count_files(self):
		return len(self.file_set.all())

	def count_bookmarks(self):
		return len(Bookmark.objects.filter(creator=self))

	def count_favorites(self):
		return len(self.favorites.all())

	def ostatus(self):
		construct_dictionary = super(Article, self).ostatus()
		construct_dictionary.update({'display name':self.title,
					     'avatar':self.avatar,
					     'objecttype':'http://activitystrea.ms/schema/1.0/person'})
		return construct_dictionary

	def make_new_activity(self, activityobject, target=None):
		entry = ActivityEntry.objects.create(actor=self,activityobject=activityobject, target=target)
		return entry

	def mark_as_favorite(self, activityobject):
		entry = self.make_new_activity(activityobject)
		entry.verb = 'http://activitystrea.ms/schema/1.0/favorite'
		entry.set_title_summary('%s marked %s as a favorite')
		entry.save()

		user = self.get_userprofile()
		user.favorites.add(activityobject)

	def start_following(self, activityobject): 
		entry = self.make_new_activity(activityobject)
		entry.verb = 'http://activitystrea.ms/schema/1.0/follow'
		entry.set_title_summary('%s is now following %s')
		entry.save()
		
	def mark_as_like(self, activityobject): 
		entry = self.make_new_activity(activityobject)
		entry.verb = 'http://activitystrea.ms/schema/1.0/like'
		entry.set_title_summary('%s likes %s')
		entry.save()

	def make_friend(self, person):
		if isinstance(person, Person):
			entry = self.make_new_activity(person)
			entry.verb = 'http://activitystrea.ms/schema/1.0/make-friend'
			entry.set_title_summary('%s and %s became friends')
			entry.save()

			user = get_userprofile()
			user.friends.add(person)

		else:
			pass

	def join_group(self, group):
		if isinstance(group, Group):
			entry = self.make_new_activity(group)
			entry.verb = 'http://activitystrea.ms/schema/1.0/join'
			entry.set_title_summary('%s joined a group named %s')
			entry.save()

			user = get_userprofile()
			user.groups.add(group)
		else:
			pass

	def play(self, activityobject):
		entry = self.make_new_activity(activityobject)
		entry.verb = 'http://activitystrea.ms/schema/1.0/play'
		entry.set_title_summary('%s played %s')
		entry.save()

	def post(self, activityobject, target=None):
		entry = self.make_new_activity(activityobject, target)
		entry.verb = 'http://activitystrea.ms/schema/1.0/post'		
		entry.set_title_summary(' '.join(['%s posted a new', activityobject.__class__.__name__.lower(),  'titled "%s"'])) 
		entry.save()

	def user_save(self, activityobject):
		entry = self.make_new_activity(activityobject)
		entry.verb = 'http://activitystrea.ms/schema/1.0/save'
		entry.set_title_summary('%s saved %s')
		entry.save()

		user = get_userprofile()
		user.saved_objects.add(activityobject)

	def share(self, activityobject): 
		entry = self.make_new_activity(activityobject)
		entry.verb = 'http://activitystrea.ms/schema/1.0/share'
		entry.set_title_summary('%s shared %s')
		entry.save()

	def tag(self, activityobject, target=None):
		entry = self.make_new_activity(activityobject, target)
		entry.verb = 'http://activitystrea.ms/schema/1.0/tag'
		entry.set_title_summary('%s tagged %s')
		entry.save()
		# Update activityobject
		activityobject.save()

	def update(self, activityobject):
		entry = self.make_new_activity(activityobject)
		entry.verb = 'http://activitystrea.ms/schema/1.0/update'
		# Special case if updating own profile
		if self == activityobject:
			entry.title = '%s updated personal profile' % (self)
			entry.summary = '%s updated <a href="%s">personal profile</a>' % (self.title_link(), self.permalink)
		else:
			entry.set_title_summary('%s updated %s')
		entry.save()


"""
Redesigned model for article. Article object and ostatus activity stream object
in the same model. Now that makes things simple.
"""
class Article(ActivityConstruct):
	summary = models.TextField(blank=True, null=True)
	content = models.TextField()

	author = models.CharField(max_length=256, blank=True, null=True)
	other_creators = models.ManyToManyField(Person, blank=True, null=True)

	license = models.ForeignKey(License, verbose_name='höfundaréttarleyfi')

	def ostatus(self):
		construct_dictionary = super(Article, self).ostatus()
		construct_dictionary.update({'summary':self.summary,
					     'content':self.content,
					     'objecttype':'http://activitystrea.ms/schema/1.0/article'})
		return construct_dictionary


class Audio(ActivityConstruct):
	audio_stream = models.URLField()
	player_applet = models.URLField(blank=True, null=True)
	description = models.TextField(blank=True, null=True)

	author = models.CharField(max_length=256, blank=True, null=True)
	other_creators = models.ManyToManyField(Person, blank=True, null=True)

	license = models.ForeignKey(License)

	def ostatus(self):
		construct_dictionary = super(Audio, self).ostatus()
		construct_dictionary.update({'audio stream':self.audio_stream,
					     'audio page':self.permalink,
					     'player applet':self.player_applet,
					     'description':self.description,
					     'object_type':'http://activitystrea.ms/schema/1.0/audio'})
		return construct_dictionary

class Bookmark(ActivityConstruct):
	target_url = models.URLField()
	thumbnail = models.URLField(blank=True, null=True)
	description = models.TextField('lýsing', blank=True, null=True)

	def __unicode__(self):
		return self.title

	def ostatus(self):
		construct_dictionary = super(Bookmark, self).ostatus()
		construct_dictionary.update({'target url':self.target_url,
					     'target title':self.title,
					     'thumbnail':self.thumbnail,
					     'description':self.description,
					     'object_type':'http://activitystrea.ms/schema/1.0/bookmark'})
		return construct_dictionary

	def _get_title(self, element):
		# Find title based on the following order:
		#   1. Open Graph protocol title (facebook)
		#   2. Meta title
		#   3. HTML title
		#   4. Return default

		title = element.cssselect('meta[property="og:title"]')
		if title:
			return title[0].attrib['content']
		
		title = element.cssselect('meta[name="title"]')
		if title:
			return title[0].attrib['content']

		title = element.cssselect('title')
		if title:
			return title[0].text_content()

		return self.target_url

	def _get_thumbnail(self, element):
		# Find image according to the following order:
		#   1. Open Graph protocol image (facebook)
		#   2. Get the largest image on the site
		
		images = element.cssselect('meta[property="og:image"]')
		if images:
			return images[0].attrib['content']
		
		images = element.cssselect('img')
		url_parts = urlparse.urlparse(self.target_url)
		
		# Create storage variables for the image we choose as thumbnail
		winning_size = 0
		winning_url = None
		
		for image in images:
			# Create a full path URI to fetch images
			uri = urlparse.urljoin(self.target_url, image.attrib['src'])

			# Compare sizes and find the largest image
			# Assume we want the largest image
			file = urllib.urlopen(uri)
			size = file.headers.get("content-length")
			if size: 
				if int(size) > winning_size:
					winning_url = uri
					winning_size = int(size)
			file.close()

		return winning_url

	def _get_description(self, element):
		# Find image according to the following order:
		#   1. Open Graph protocol description (facebook)
		#   2. Get meta description
		#   3. URL will have to suffice as description
		
		description = element.cssselect('meta[property="og:description"]')
		if description:
			return description[0].attrib['content']

		description = element.cssselect('meta[name="description"]')
		if description:
			return description[0].attrib['content']

		return ''

	def fetch_information(bookmark):
		# Get information to populate
		# Returns the following variables (set or default):
		title = bookmark.target_url
		description = bookmark.description

		# Using public domain spiderweb for now
		# Make configurable?
		thumbnail = 'http://www.openclipart.org/image/800px/svg_to_png/Halloween_Spider_Web_Icon.png'

		try:
			# Parse site
			parsed = lxml.html.parse(bookmark.target_url).getroot()
		
			# Try to find the title within the target page
			title = bookmark._get_title(parsed)
			
			if not description:
				description = bookmark._get_description(parsed)
			
			thumbnail = bookmark._get_thumbnail(parsed)
		except:
			pass

		# Limit title to 256 characters
		return (title[:256], description, thumbnail)

	def save(self, *args, **kwargs):
		(self.title, self.description, self.thumbnail) = self.fetch_information()
		super(Bookmark, self).save(*args, **kwargs)

class Comment(ActivityConstruct):
	content = models.TextField()
	parent = models.ForeignKey(ActivityConstruct, related_name='comments')

	def ostatus(self):
		construct_dictionary = super(Comment, self).ostatus()
		construct_dictionary.update({'subject':self.title,
					     'content':self.content,
					     'thr:in-reply-to':self.parent.permalink,
					     'objecttype':'http://activitystrea.ms/schema/1.0/comment'})
		return construct_dictionary

	def save(self, *args, **kwargs):
		super(Comment, self).save(*args, **kwargs)
		# Update parent
		self.parent.save()

class Group(ActivityConstruct):
	avatar = models.URLField()
	description = models.TextField(blank=True, null=True)

	def ostatus(self):
		construct_dictionary = super(Group, self).ostatus()
		construct_dictionary.update({'display_name':self.title,
					     'avatar':self.avatar,
					     'objecttype':'http://activitystrea.ms/schema/1.0/group'})
		return construct_dictionary

class Note(ActivityConstruct):
	license= models.ForeignKey(License, editable=False)

	def ostatus(self):
		construct_dictionary = super(Note, self).ostatus()
		construct_dictionary.update({'content':self.title,
					     'objecttype':'http://activitystrea.ms/schema/1.0/note'})
		return construct_dictionary

class File(models.Model):
	associated_file_url = models.URLField()
	mimetype = models.CharField(max_length=128, blank=True, null=True)

	description = models.TextField(blank=True, null=True)

	license = models.ForeignKey(License)

	author = models.CharField(max_length=256, blank=True, null=True)
	other_creators = models.ManyToManyField(Person, blank=True, null=True)

	def ostatus(self):
		construct_dictionary = super(File, self).ostatus()
		construct_dictionary.update({'associated file url':self.associated_file_url,
					     'mimetype':self.mimetype,
					     'objecttype':'http://activitystrea.ms/schema/1.0/file'})
		return construct_dictionary

class PhotoAlbum(ActivityConstruct):
	description = models.TextField()
	thumbnail = models.URLField()

	def ostatus(self):
		construct_dictionary = super(PhotoAlbum, self).ostatus()
		construct_dictionary.update({'thumbnail':self.thumbnail,
					     'album page':self.permalink,
					     'object_type':'http://activitystrea.ms/schema/1.0/photo-album'})
		return construct_dictionary

class Photo(ActivityConstruct):
	thumbnail = models.URLField()
	larger_image = models.URLField()

	description = models.TextField(blank=True, null=True)
	album = models.ForeignKey(PhotoAlbum, related_name='photos', blank=True, null=True)
	license = models.ForeignKey(License, verbose_name='höfundaréttarleyfi')

	author = models.CharField(max_length=256, blank=True, null=True)
	other_creators = models.ManyToManyField(Person, blank=True, null=True)

	def ostatus(self):
		construct_dictionary = super(Photo, self).ostatus()
		construct_dictionary.update({'thumbnail':self.thumbnail,
					     'larger image':self.larger_image,
					     'image page':self.permalink,
					     'description':self.description,
					     'content':self.description,
					     'objecttype':'http://activitystrea.ms/schema/1.0/photo'})
		return construct_dictionary


class Video(ActivityConstruct):
	video_stream = models.URLField()
	thumbnail = models.URLField()
	player_applet = models.URLField(blank=True, null=True)

	description = models.TextField('lýsing', blank=True, null=True)

	license = models.ForeignKey(License)

	author = models.CharField(max_length=256, blank=True, null=True)
	other_creators = models.ManyToManyField(Person, blank=True, null=True)

	def ostatus(self):
		construct_dictionary = super(Video, self).ostatus()
		construct_dictionary.update({'thumbnail':self.thumbnail,
					     'video stream':self.video_stream,
					     'player applet':self.player_applet,
					     'video page':self.permalink,
					     'description':self.description,
					     'content':self.description,
					     'objecttype':'http://activitystrea.ms/schema/1.0/video'})
		return construct_dictionary	



# Not strictly in activitystreams

class Event(models.Model):
	title = models.CharField(max_length=128)
	slug = models.CharField(max_length=256, editable=False)
	description = models.TextField()
	location = models.CharField(max_length=256)
	creator = models.ForeignKey(User)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	start_date = models.DateTimeField()
	end_date = models.DateTimeField(blank=True, null=True)

	def __unicode__(self):
		return self.title

	def save(self, *args, **kwargs):
		self.slug = slugicefy(self.title)
		super(Event, self).save(*args, **kwargs)

class Question(models.Model):
	title = models.CharField('spurning', max_length=128, blank=True, default='')
	slug = models.SlugField(max_length=256, editable=False)
	description = models.TextField('nánari lýsing', blank=True, null=True)
	creator = models.ForeignKey(User, editable=False)
	created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.title

	def save(self, *args, **kwargs):
		if self.title == '':
			self.title = '%s...?' % (self.description[:124])
		self.slug = slugicefy(self.title)
		if not self.creator:
			self.creator = User.objects.get(pk=1)
		super(Question, self).save(*args, **kwargs)

class Answer(models.Model):
	title = models.CharField(max_length=256, blank=True, null=True)
	question = models.ForeignKey(Question)
	slug = models.SlugField(max_length=256, editable=False)
	description = models.TextField()
	creator = models.ForeignKey(User, editable=False)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		if self.title:
			return self.title
		else:
			return 'Answer to: %s' % (self.question.title)

	def save(self, *args, **kwargs):
		if self.title == '':
			self.title = '%s...?' % (self.description[:124])

		self.slug = slugicefy(self.title)
		self.creator = User.objects.get(pk=1)
		
		super(Answer, self).save(*args, **kwargs)

class Tag(models.Model):
	tag = models.CharField(max_length=32)
	slug = models.SlugField(editable=False)
	creator = models.ForeignKey(Person, editable=False, related_name='tagger')
	target = models.ForeignKey(ActivityConstruct, related_name='tag_set')
	created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.tag

	def save(self, *args, **kwargs):
		self.tag = self.tag.lower()
		self.slug = slugicefy(self.tag)
		super(Tag, self).save(*args, **kwargs)
		self.creator.tag(self.target)

class PrivateMessage(models.Model):
	recipient = models.ForeignKey(Person, verbose_name=_('recipient'), related_name='recipients')
	# We let sender be an activity construct since we want groups to be
	# able to act as senders
	sender = models.ForeignKey(ActivityConstruct, verbose_name=_('sender'), related_name='senders', editable=False)
	subject = models.CharField(max_length=128, verbose_name=_('subject'))
	content = models.TextField(verbose_name=_('content'))
	time = models.DateTimeField(editable=False, default=datetime.now)
	read = models.BooleanField(editable=False, default=False)
	
	def __unicode__(self):
		return self.subject

	class Meta:
		ordering = ('read', '-time',)

class Search(models.Model):
	searchstring = models.CharField(max_length=512)
	searcher = models.ForeignKey(User, editable=False)
	created = models.DateTimeField(auto_now_add=True)
	results = models.TextField()
	tag = models.ManyToManyField(Tag)

	def __unicode__(self):
		return self.searchstring

post_save.connect(create_userprofile, sender=User)
