from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('registration.backends.default.urls')),
    (r'^static/(?P<path>.*)', 'django.views.static.serve', {'document_root': '/home/sesarr/Work/razpilnik/static'}),
    (r'', include('razpilnik.squeal.urls'))
)
