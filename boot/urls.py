# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}),
    url(r'^(?P<mac_addr>.+)/pxelinux.cfg/(?P<cfg_name>.+)/$',
        'objects.views.serve_config'),
    url(r'^(?P<mac_addr>.+)/pxelinux.cfg/(?P<cfg_name>.+)$',
        'objects.views.serve_config'),
    url(r'^media/(?P<filename>.*)$', 'objects.views.serve_file'),
    url(r'^(.*)/(?P<filename>.*)$', 'objects.views.serve_file')
)
