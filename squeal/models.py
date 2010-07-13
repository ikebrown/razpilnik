# -*- coding: utf-8 -*-
try:
 from cStringIO import StringIO
except ImportError:
 from StringIO import StringIO

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

from PIL import Image
from django.db.models.fields.files import ImageField, ImageFieldFile
from django.core.files.base import ContentFile
from registration.signals import user_activated, user_registered

def _update_extension(filename, new_ext):
    parts = filename.split('.')
    parts[-1] = new_ext
    return '.'.join(parts)

class ResizedImageFieldFile(ImageFieldFile):
 def save(self, name, content, save=True):
  new_content = StringIO()
  content.file.seek(0)

  img = Image.open(content.file)
  img.thumbnail((
     self.field.max_width, 
     self.field.max_height
  ), Image.ANTIALIAS)
  img.save(new_content, format=self.field.format)

  new_content = ContentFile(new_content.getvalue())
  new_name = _update_extension(name, self.field.format.lower())

  super(ResizedImageFieldFile, self).save(new_name, new_content, save)

class ResizedImageField(ImageField):
 attr_class = ResizedImageFieldFile
 def __init__(self, max_width=100, max_height=100, format='PNG', *args, **kwargs):
  self.max_width = max_width
  self.max_height = max_height
  self.format = format
  super(ResizedImageField, self).__init__(*args, **kwargs)
  
class Squealer(models.Model):
 user = models.OneToOneField(User, related_name="users")
 avatar = ResizedImageField(max_width=130, max_height=130, upload_to="avatars/", blank=True)
 location = models.CharField(max_length=64, blank=True)
 bio = models.CharField(max_length=140, blank=True)
 website = models.URLField(max_length=64, blank=True)
 following = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='followers')

 def save(self, *args, **kwargs):
  try:
   existing = Squealer.objects.get(user=self.user)
   self.id = existing.id #force update instead of insert
  except Squealer.DoesNotExist: pass 
  models.Model.save(self, *args, **kwargs)

 def __unicode__(self):
  return (self.user.first_name or self.user.username) + " " + self.user.last_name

class Squeal(models.Model):
 author = models.ForeignKey(Squealer, related_name="authors")
 content = models.CharField(max_length=140)
 pub_date = models.DateTimeField("date published", default=datetime.now)

 class Meta:
  ordering = ['-pub_date', 'author']
 
 def __unicode__(self):
  return self.author.user.username + ": " + self.content[:64] + "..."

# Signal handlers
def create_squealer(sender, user, request, **kwargs):
  squealer = Squealer(user=user)
  squealer.save()

user_registered.connect(create_squealer)
