from django.db import models
from django.conf import settings
from django.core.exceptions import *
import os

class Command(models.Model):
    def __unicode__(self):
        return self.name
    name = models.CharField(max_length=64)

class MenuItem(models.Model):
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
    def __unicode__(self):
        return self.name
    more = models.CharField(max_length=32768)
    name = models.CharField(max_length=64)
    menuItem = models.ManyToManyField(MenuItem)

class Group(models.Model):
    def __unicode__(self):
        return self.name
    name = models.CharField(max_length=64)
    config = models.ForeignKey(Config)

class Machine(models.Model):
    def __unicode__(self):
        return self.name
    def save(self, force_insert=False, force_update=False):
        self.mac = self.mac.lower()
        super(Machine, self).save(force_insert, force_update)
    name = models.CharField(max_length=64)
    mac = models.CharField(max_length=17)
    group = models.ForeignKey(Group)

class File(models.Model):
    def __unicode__(self):
        return self.name
    def save(self, force_insert=False, force_update=False):
        try:
            oldFile = File.objects.get(pk=self.pk)
            os.remove(oldFile.fileItem.name)
        except File.DoesNotExist:
            pass
        finally:
            super(File, self).save(force_insert, force_update)
    name = models.CharField(max_length=64)
    fileItem = models.FileField(upload_to=settings.MEDIA_ROOT)
