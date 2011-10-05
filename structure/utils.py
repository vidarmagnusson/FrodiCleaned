# -*- encoding: utf-8 -*-
from django.template.defaultfilters import slugify
from django.conf import settings
# import tweepy
import urllib
import simplejson

def slugicefy(value):
	value = value.replace(u'þ','th')
	value = value.replace(u'Þ','Th')
	value = value.replace(u'æ','ae')
	value = value.replace(u'Æ','Ae')
	value = value.replace(u'ð','d')
	value = value.replace(u'Ð','D')
	return slugify(value)

def shorten_url(url):
	if settings.BITLY_USER and settings.BITLY_APIKEY:
		data = {'login':settings.BITLY_USER, 'apiKey':settings.BITLY_APIKEY, 'format':'json', 'longUrl':url}
		encoded_data = urllib.urlencode(data)
		website = urllib.urlopen("http://api.bitly.com/v3/shorten?%s" % (encoded_data))
		json = website.read()
		bitly = simplejson.loads(json)
		if bitly['status_code'] == 200:
			return bitly['data']['url']

	return url
       
"""
A method to create a cloud based on a list of elements and buckets
The list of element includes the elements that will make up the cloud
The buckets variable is a list of different sizes (can be strings)
Returns a sorted list of dictionaries:
[{element:"which element",size:"relative size"}]
"""
def cloudify(elements, buckets):
	# We return an empty list if there are no elements
	if len(elements) == 0:
		return []
	# Number of buckets to fill
	bucket_count = len(buckets)

	# What element is the least number of in the list
	least_of = elements.count(min(elements, key=elements.count))
	# Normalised "most of" (start count from zero)
	# We make it a float to force float division later
	most_of = float(elements.count(max(elements, key=elements.count))-least_of)

	# If least of is same as most of we return all elements in
	# the average position (about half way rounded down)
	if most_of == 0.0:
		size = buckets[bucket_count/2]
		return [{'element':element,'size':size} for element in sorted(set(elements))]

	# Find the position (which bucket) of every element based on
	# percentage of normalised "most of" (rounded and 'integerised')
	# Fill in the results dictionary
	results = {}
	for element in set(elements):
		percentage = (elements.count(element)-least_of) / most_of
		bucket_position = int(round(percentage*(bucket_count-1)))
		results[element] = buckets[bucket_position]

	return [{'element':key,'size':results[key]} for key in sorted(results.keys())]

# Not being used, kept here in case it is needed for a bridge
# between Twitter and Frodi
#
#def dent(prefix, msg, url):
#	if (settings.TWITTER_CONSUMER_KEY and settings.TWITTER_CONSUMER_SECRET and settings.TWITTER_ACCESS_TOKEN_KEY and settings.TWITTER_ACCESS_TOKEN_SECRET):
#		prefixed_msg = '%s: %s' % (prefix, msg)
#		if len(prefixed_msg) > 119:
#			prefixed_msg = '%s...' % prefixed_msg[:116]
#
#		status = '%s %s' % (prefixed_msg, shorten_url(url))
#	
#		auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
#		auth.set_access_token(settings.TWITTER_ACCESS_TOKEN_KEY, settings.TWITTER_ACCESS_TOKEN_SECRET)
#		api = tweepy.API(auth)
#		returned_status = api.update_status(status)
#		return returned_status
#
#	return None
