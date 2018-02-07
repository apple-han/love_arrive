# -*- coding: utf-8 -*-
__author__ = '__apple'
__time__ = '2018/1/30 11:16'

from __future__ import absolute_import

import os
import django

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'love_arrive.settings')
django.setup()

app = Celery('love_arrive')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)