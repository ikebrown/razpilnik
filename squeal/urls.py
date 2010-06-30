from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('razpilnik.squeal.views',
      (r'^$', 'index'),
      (r'^(?P<squealer>\w+)/$', 'squealer')
)

