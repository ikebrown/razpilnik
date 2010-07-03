from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('registration.backends.default.urls')),
    (r'^static/(?P<path>.*)', 'django.views.static.serve', {'document_root': '/home/sesarr/Work/razpilnik/static'}),
    (r'', include('razpilnik.squeal.urls'))
    # Example:
    # (r'^razpilnik/', include('razpilnik.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
)
