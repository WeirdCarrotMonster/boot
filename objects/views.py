from objects.models import *
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper

def serveConfig(request, mac_addr, cfg_name):
	try:
		machine = Machine.objects.get(mac=mac_addr.lower())
		config = machine.group.config
		return render_to_response("config.html", {"menuItems":config.menuItem.all(), "config":config})
	except:
		try:
			config = Config.objects.get(name="fallback")
			return render_to_response("config.html", {"menuItems":config.menuItem.all(), "config":config})
		except:
			return HttpResponse("")

def serveFile(request, filename):
	try:
		fileObject = File.objects.get(name=filename)
		wrapper = FileWrapper(file(fileObject.fileItem.name))
		response = HttpResponse(wrapper, content_type='application/octet-stream')
		response['Content-Length'] = fileObject.fileItem.size
		return response
		pass
	except Exception, e:
		return HttpResponse("")
