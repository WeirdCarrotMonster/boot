# coding=utf-8
from django.db import models
from django.conf import settings
import os


class Command(models.Model):
    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команды"

    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=64)


class MenuItem(models.Model):
    class Meta:
        verbose_name = "Элемент меню"
        verbose_name_plural = "Элементы меню"

    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=64)


class ConfigItem(models.Model):
    def __unicode__(self):
        return self.command.name + " " + self.args

    command = models.ForeignKey(Command)
    menuItem = models.ForeignKey(MenuItem)
    args = models.CharField(max_length=1024)


class Config(models.Model):
    class Meta:
        verbose_name = "Файл конфигурации"
        verbose_name_plural = "Файлы конфигурации"

    def __unicode__(self):
        return self.name

    more = models.CharField(max_length=32768)
    name = models.CharField(max_length=64)
    menuItem = models.ManyToManyField(MenuItem, null=True, blank=True)


class Group(models.Model):
    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=64)
    config = models.ForeignKey(Config)


class Machine(models.Model):
    class Meta:
        verbose_name = "Машина"
        verbose_name_plural = "Машины"

    def __unicode__(self):
        return self.name

    def save(self, force_insert=False, force_update=False):
        self.mac = self.mac.lower()
        super(Machine, self).save(force_insert, force_update)

    name = models.CharField(max_length=64)
    mac = models.CharField(max_length=17)
    group = models.ForeignKey(Group)


class File(models.Model):
    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"

    def __unicode__(self):
        return self.name

    def save(self, force_insert=False, force_update=False):
        path = os.path.join(settings.MEDIA_ROOT, "files", self.fileItem.name)
        if os.path.exists(path):
            os.remove(path)
        super(File, self).save(force_insert, force_update)

    name = models.CharField(max_length=64)
    fileItem = models.FileField(upload_to="files")
