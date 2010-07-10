from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

from django.db.models.signals import post_save

class Squealer(models.Model):
 user = models.OneToOneField(User, related_name="users")
 location = models.CharField(max_length=64, blank=True)
 bio = models.CharField(max_length=140, blank=True)
 website = models.URLField(max_length=64, blank=True)
 following = models.ManyToManyField('self', blank=True, related_name='followers')
 def __unicode__(self):
  return (self.user.first_name or self.user.username) + " " + self.user.last_name

class Squeal(models.Model):
 author = models.OneToOneField(Squealer, related_name="authors")
 content = models.CharField(max_length=140)
 pub_date = models.DateTimeField("date published", default=datetime.now)

 class Meta:
  ordering = ['-pub_date', 'author']
 
 def __unicode__(self):
  return self.author.user.username + ": " + self.content[:64] + "..."

# Signal handlers

def create_squealer(sender, created, instance, **kwargs):
  if not created: return
  squealer = Squealer(user=instance)
  squealer.save()

post_save.connect(create_squealer, sender=User)
