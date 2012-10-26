from django.db import models
from django.conf import settings

class Command(models.Model):
    def __unicode__(self):
        return self.name
    name = models.CharField(max_length=16)

class MenuItem(models.Model):
    def __unicode__(self):
        return self.name
    name = models.CharField(max_length=32)

class ConfigItem(models.Model):
    def __unicode__(self):
        return self.command.name + " " + self.args
    command = models.ForeignKey(Command)
    menuItem = models.ForeignKey(MenuItem)
    args = models.CharField(max_length=32)
   
class Config(models.Model):
    def __unicode__(self):
        return self.name
    more = models.CharField(max_length=512)
    name = models.CharField(max_length=32)
    menuItem = models.ManyToManyField(MenuItem)

class Group(models.Model):
    def __unicode__(self):
        return self.name
    name = models.CharField(max_length=32)
    config = models.ForeignKey(Config)

class Machine(models.Model):
    def __unicode__(self):
        return self.name
    name = models.CharField(max_length=32)
    mac = models.CharField(max_length=12)
    group = models.ForeignKey(Group)

class File(models.Model):
    def __unicode__(self):
        return self.name
    name = models.CharField(max_length=32)
    kernelFile = models.FileField(upload_to=settings.MEDIA_ROOT)
