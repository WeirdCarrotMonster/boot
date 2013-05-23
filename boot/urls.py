# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       # Админка
                       url(r'^admin/', include(admin.site.urls)),
                       # Статика и файлы
                       (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
                       # Конфиги
                       url(r'^(?P<mac_addr>.+)/pxelinux.cfg/(?P<cfg_name>.+)/$', 'objects.views.serveConfig'),
                       url(r'^(?P<mac_addr>.+)/pxelinux.cfg/(?P<cfg_name>.+)$', 'objects.views.serveConfig'),
                       #WAT-mode engaged
                       # Файлы
                       url(r'^media/(?P<filename>.*)$', 'objects.views.serveFile'),
                       url(r'^(.*)/(?P<filename>.*)$', 'objects.views.serveFile'),
)
