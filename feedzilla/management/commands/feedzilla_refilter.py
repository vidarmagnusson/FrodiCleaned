# Copyright: 2011, Grigoriy Petukhov
# Author: Grigoriy Petukhov (http://lorien.name)
# License: BSD
from datetime import datetime

from django.core.management.base import BaseCommand

from feedzilla.models import Post

class Command(BaseCommand):
    help = u'Refilter posts'

    def handle(self, *args, **kwargs):
        posts = Post.objects.all()
        if args:
            query = args[0]
            posts = posts.filter(feed__site_url__icontains=query)

        for post in posts:
            post.save()

        print '%d posts processed' % posts.count()
