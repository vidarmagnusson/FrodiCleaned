# -*- coding: utf-8 -*-
# Copyright: 2011, Grigoriy Petukhov
# Author: Grigoriy Petukhov (http://lorien.name)
# License: BSD
from datetime import datetime
import re

from django.core.management.base import BaseCommand
from django.conf import settings

from feedzilla.utils.parse import parse_feed
from feedzilla.models import Feed, Post
from feedzilla import settings

class Command(BaseCommand):
    help = u'Update feeds'

    def handle(self, *args, **kwargs):
        qs = Feed.objects.all()
        if len(args):
            qs = qs.filter(feed_url__icontains=args[0])

        for feed in qs:
            resp = parse_feed(feed.feed_url, etag=feed.etag,
                              summary_size=settings.FEEDZILLA_SUMMARY_SIZE)
            if not resp['success']:
		pass
            else:
                new_posts = 0
                for entry in resp['entries']:

                    try:
                        Post.objects.get(guid=entry['guid'])
                    except Post.DoesNotExist:

                        post = Post(
                            feed=feed,
                            title=entry['title'],
                            content=entry['content'],
                            summary=entry['summary'],
                            link=entry['link'],
                            guid=entry['guid'],
                            created=entry['created']
                        )
                        post.save()

                        new_posts += 1

            feed.last_checked = datetime.now()
            feed.save()
            feed.update_counts()
