# coding=utf-8

from django.contrib import admin
from objects.models import *
from django import forms


class ConfigForm(forms.ModelForm):
    template = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Config


class ConfigAdmin(admin.ModelAdmin):
    form = ConfigForm
    readonly_fields = ('preview',)
    filter_horizontal = ('menuItems',)

    def preview(self, obj):
        try:
            return obj.render()
        except Exception as e:
            return "Не удалось показать предварительный просмотр: {}".format(str(e))

    preview.short_description = "Результат"


class MenuItemValueInline(admin.StackedInline):
    model = MenuItemValue
    extra = 1
    list_display = ("name",)


class MenuItemForm(forms.ModelForm):
    template = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = MenuItem


class MenuItemAdmin(admin.ModelAdmin):
    form = MenuItemForm
    list_display = ('name',)
    readonly_fields = ('preview',)

    def preview(self, obj):
        try:
            return obj
        except:
            return "Не удалось показать предварительный просмотр"

    preview.short_description = "Результат"

    inlines = [MenuItemValueInline]


class MachineAdmin(admin.ModelAdmin):
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.group:
            return obj.group.config.render()
        else:
            try:
                return Config.objects.get(name="default").render()
            except Config.DoesNotExist:
                return "Машина не имеет конфигурации"

    preview.short_description = "Конфигурация загрузки"

    list_display = ('name', 'group')
    list_editable = ('group',)
    list_filter = ('group',)


class GlobalValueAdmin(admin.ModelAdmin):
    list_display = ('id', 'key', 'value')
    list_editable = ('key', 'value')


class MachineInline(admin.StackedInline):
    model = Machine
    extra = 1


class GroupAdmin(admin.ModelAdmin):
    def machines_list(self):
        html = ""
        for obj in Machine.objects.filter(group_id=self.id):
            html += '<p><a href="/admin/objects/machine/%s/">%s</a></p>' % (obj.id, obj.name)
        return html
    machines_list.allow_tags = True

    list_display = ['name', machines_list]
    list_filter = ['name']

admin.site.register(GlobalValue, GlobalValueAdmin)
admin.site.register(Config, ConfigAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Machine, MachineAdmin)
admin.site.register(File)
