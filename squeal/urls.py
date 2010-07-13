# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('razpilnik.squeal.views',
      (r'^$', 'index'),
      (r'^home/$', 'home'),
      (r'^(?P<squealer>\w+)/$', 'squealer'),
      #(r'^(?P<squealer>\w+)/settings$', 'settings'),
      (r'^(?P<squealer>\w+)/squeal/(?P<squeal_id>\d+)/$', 'squeal'),
      (r'^(?P<squealer>\w+)/squeal/delete/(?P<squeal_id>\d+)/$', 'squeal_delete'),
      (r'^accounts/settings/$', 'settings'),
      (r'^follow/(?P<to_follow>\w+)/$', 'follow'),
      (r'^unfollow/(?P<to_follow>\w+)/$', 'unfollow'),
)
