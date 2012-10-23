from objects.models import *
from django.shortcuts import render_to_response

def getConfig(request, mac_addr, cfg_name):
	machine = Machine.objects.get(mac=mac_addr)
	if machine is not None:
		config = machine.group.config
	else:
		config = Config.objects.get(name="fallback")

	return render_to_response("config.html", {"menuItems":config.menuItem.all()})
