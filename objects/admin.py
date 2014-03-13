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
    list_display = ('name', 'group')
    list_editable = ('group',)


class GlobalValueAdmin(admin.ModelAdmin):
    list_display = ('id', 'key', 'value')
    list_editable = ('key', 'value')

admin.site.register(GlobalValue, GlobalValueAdmin)
admin.site.register(Config, ConfigAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Group)
admin.site.register(Machine, MachineAdmin)
admin.site.register(File)
