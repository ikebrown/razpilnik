from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('razpilnik.login.views',
      (r'^$', 'login'),
      (r'^signup/$', 'signup'),
      (r'^logout/$', 'logout')
)

