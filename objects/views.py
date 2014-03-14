# coding=utf-8

from objects.models import *
from django.http import HttpResponse
from django.conf import settings
import os


def serve_config(request, mac_addr, cfg_name):
    try:
        machine = Machine.objects.get(mac=mac_addr.lower())
        if cfg_name == "default":
            config = machine.group.config
        else:
            config = Config.objects.get(name=cfg_name)
        return HttpResponse(config.render())
    except:
        try:
            defaultGroup = Group.objects.get(name="default")
            config = defaultGroup.config
            return HttpResponse(config.render())
        except Group.DoesNotExist:
            return HttpResponse("")


def serve_file(request, filename):
    file_paths = [
        os.path.join(settings.MEDIA_ROOT, filename),
        os.path.join(settings.MEDIA_ROOT_FALLBACK, filename)
    ]

    for path in file_paths:
        if os.path.isfile(path):
            fsock = open(path, "r")
            response = HttpResponse(
                fsock,
                content_type='application/octet-stream')
            response['Content-Length'] = os.path.getsize(path)
            return response
    return HttpResponse("")
