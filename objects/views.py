from objects.models import *
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper


def serveConfig(request, mac_addr, cfg_name):
    try:
        machine = Machine.objects.get(mac=mac_addr.lower())
        if cfg_name == "default":
            config = machine.group.config
        else:
            config = Config.objects.get(name=cfg_name)
        return render_to_response("config.html", {"menuItems": config.menuItem.all(), "config": config})
    except:
        try:
            defaultGroup = Group.objects.get(id=1)
            config = defaultGroup.config
            return render_to_response("config.html", {"menuItems": config.menuItem.all(), "config": config})
        except Group.DoesNotExist:
            return HttpResponse("")


def serveFile(request, filename):
    try:
        fileObject = File.objects.get(name=filename)
        wrapper = FileWrapper(file(fileObject.fileItem.name))
        response = HttpResponse(wrapper, content_type='application/octet-stream')
        response['Content-Length'] = fileObject.fileItem.size
        return response
        pass
    except:
        return HttpResponse("")
