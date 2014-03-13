# coding=utf-8

from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.conf import settings
from django.template import Context, Template
import os


@python_2_unicode_compatible
class GlobalValue(models.Model):
    class Meta:
        verbose_name = "Глобальное значение"
        verbose_name_plural = "Глобальные значения"

    def __str__(self):
        return self.value

    key = models.CharField(
        verbose_name="Ключ",
        null=False,
        blank=False,
        unique=True,
        max_length=64)
    value = models.CharField(
        verbose_name="Значение",
        null=True,
        blank=True,
        max_length=64)


@python_2_unicode_compatible
class MenuItem(models.Model):
    class Meta:
        verbose_name = "Элемент меню"
        verbose_name_plural = "Элементы меню"

    def __str__(self):
        return self.name

    def render(self):
        t = Template(self.template)

        #TODO: переписать через values() и генератор
        local_values = {}
        for val in self.menuitemvalue_set.all():
            local_values[val.key] = val.value

        global_values = {}
        for val in GlobalValue.objects.all():
            global_values[val.key] = val.value

        c = Context({
            "GLOBAL": global_values,
            "LOCAL": local_values
        })
        return t.render(c)

    name = models.CharField(
        verbose_name="Имя",
        unique=True,
        max_length=64)
    template = models.CharField(
        verbose_name="Шаблон",
        max_length=512)


@python_2_unicode_compatible
class MenuItemValue(models.Model):
    class Meta:
        verbose_name = "Значение переменной элемента меню"
        verbose_name_plural = "Значение переменной элемента меню"

    def __str__(self):
        return self.value

    menu = models.ForeignKey(MenuItem)
    key = models.CharField(
        verbose_name="Ключ",
        null=False,
        blank=False,
        max_length=64)
    value = models.CharField(
        verbose_name="Значение",
        null=True,
        blank=True,
        max_length=64)


@python_2_unicode_compatible
class Config(models.Model):
    class Meta:
        verbose_name = "Конфигурация"
        verbose_name_plural = "Конфигурации"

    def __str__(self):
        return self.name

    def render(self):
        t = Template(self.template)

        menu_items = self.menuItems.all()
        #TODO: переписать через values() и генератор
        global_values = {}
        for val in GlobalValue.objects.all():
            global_values[val.key] = val.value

        c = Context({
            "GLOBAL": global_values,
            "MENUITEM": menu_items
        })
        return t.render(c)

    name = models.CharField(
        verbose_name="Имя",
        max_length=64)
    template = models.CharField(
        verbose_name="Шаблон",
        max_length=2048)
    menuItems = models.ManyToManyField(
        MenuItem,
        verbose_name="Элемент меню",
        null=True,
        blank=True)


@python_2_unicode_compatible
class Group(models.Model):
    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self):
        return self.name

    name = models.CharField(
        verbose_name="Имя группы",
        max_length=64)
    config = models.ForeignKey(
        Config,
        verbose_name="Конфигурация")


@python_2_unicode_compatible
class Machine(models.Model):
    class Meta:
        verbose_name = "Машина"
        verbose_name_plural = "Машины"

    def __str__(self):
        return "{} ({})".format(self.name, self.mac)

    def save(self, *args, **kwargs):
        self.mac = self.mac.lower()
        super(Machine, self).save(*args, **kwargs)

    name = models.CharField(
        verbose_name="Имя машины",
        max_length=64)
    mac = models.CharField(
        verbose_name="MAC-адрес машины",
        max_length=17)
    group = models.ForeignKey(
        Group,
        null=True,
        verbose_name="Группа")


@python_2_unicode_compatible
class File(models.Model):
    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        path = os.path.join(settings.MEDIA_ROOT, "files", self.fileItem.name)
        if os.path.exists(path):
            os.remove(path)
        super(File, self).save(*args, **kwargs)

    name = models.CharField(
        verbose_name="Имя файла",
        max_length=64)
    fileItem = models.FileField(
        verbose_name="Файл",
        upload_to=".")
