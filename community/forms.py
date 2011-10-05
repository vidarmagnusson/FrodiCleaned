from django.forms import ModelForm
from community.models import *
from community.widgets import *

class ArticleForm(ModelForm):
	class Meta:
		model = Article

class NoteForm(ModelForm):
	class Meta:
		model = Note

class VideoForm(ModelForm):
	class Meta:
		model = Video

class AudioForm(ModelForm):
	class Meta:
		model = Audio

class FileForm(ModelForm):
	class Meta:
		model = File

class GroupForm(ModelForm):
	class Meta:
		model = Group
		exclude = ('avatar',)

class PhotoAlbumForm(ModelForm):
	class Meta:
		model = PhotoAlbum

class PhotoForm(ModelForm):
	class Meta:
		model = Photo

class PersonForm(ModelForm):
	class Meta:
		model = Person
		exclude = ('user', 'avatar', 'permalink', 'location',)
		widgets = {'school':SchoolSelection}

class BookmarkForm(ModelForm):
	class Meta:
		model = Bookmark
		exclude = ('title','thumbnail')

class QuestionForm(ModelForm):
	class Meta:
		model = Question

class AnswerForm(ModelForm):
	class Meta:
		model = Answer

class EventForm(ModelForm):
	class Meta:
		model = Event
		exclude = ('creator',)
		widgets = {'start_date':SelectStartDate(),'end_date':SelectEndDate()}
