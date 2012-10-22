from django.contrib import admin
from objects.models import *

class ConfigItemInline(admin.StackedInline):
    model = ConfigItem
    extra = 1

class MenuItemAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
    ]
    inlines = [ConfigItemInline]

admin.site.register(Config)
admin.site.register(ConfigItem)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Command)
admin.site.register(Group)
admin.site.register(Machine)
