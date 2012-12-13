from django.contrib import admin
from objects.models import *
from django import forms

class ConfigForm( forms.ModelForm ):
	name = forms.CharField()
	more = forms.CharField( widget=forms.Textarea )

class ConfigAdmin( admin.ModelAdmin ):
	form = ConfigForm

class ConfigItemInline(admin.StackedInline):
	model = ConfigItem
	extra = 1

class MenuItemAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,               {'fields': ['name']}),
	]
	inlines = [ConfigItemInline]

admin.site.register(Config, ConfigAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Command)
admin.site.register(Group)
admin.site.register(Machine)
admin.site.register(File)
