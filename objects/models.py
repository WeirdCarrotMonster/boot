from django.db import models

# Create your models here.
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
