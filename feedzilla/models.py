# -*- coding:utf-8 -*-
# Copyright: 2011, Grigoriy Petukhov
# Author: Grigoriy Petukhov (http://lorien.name)
# License: BSD
from urlparse import urlsplit

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from feedzilla.utils.clean import safe_html

class Feed(models.Model):
    feed_url = models.URLField(_('feed url'), unique=True, verify_exists=False)
    etag = models.CharField(u'ETag', max_length=255, blank=True, default='')
    last_checked = models.DateTimeField(_('last checked'), blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    post_count = models.IntegerField(blank=True, default=0)
    active_post_count = models.IntegerField(blank=True, default=0)

    def __unicode__(self):
        return self.feed_url

    def get_absolute_url(self):
        return reverse('feedzilla_feed', args=[self.id])

    def site_hostname(self):
        return urlsplit(self.feed_url).hostname

    class Meta:
        verbose_name = _('feed')
        verbose_name_plural = _('feeds')

    def update_counts(self):
        self.post_count = self.posts.count()
        self.active_post_count = self.posts.filter(active=True).count()
        self.save()


class ActivePostManager(models.Manager):
    def get_query_set(self):
        return super(ActivePostManager, self).get_query_set().filter(active=True)


class Post(models.Model):
    feed = models.ForeignKey(Feed, verbose_name=_('feed'), related_name='posts')
    title = models.CharField(_('title'), max_length=255)
    link = models.TextField(_('link'))
    summary = models.TextField(_('summary'), blank=True)
    content = models.TextField(_('content'), blank=True)
    created = models.DateTimeField(_('creation time'))
    guid = models.CharField(_('identifier'), max_length=255, unique=True)
    active = models.BooleanField(_('active'), blank=True, default=True)

    objects = models.Manager()
    active_objects = ActivePostManager()

    class Meta:
        ordering = ['-created']
        verbose_name = _('post')
        verbose_name_plural = _('posts')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return self.link

    def summary_uncached(self):
        return safe_html(self.content[:settings.FEEDZILLA_SUMMARY_SIZE])
