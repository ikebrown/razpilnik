from django.db import models
from django.contrib.auth.models import User

class Squeal(models.Model):
 author = models.ForeignKey(User, related_name="authors")
 content = models.CharField(max_length=140)
 pub_date = models.DateTimeField("date published")

 class Meta:
  ordering = ['-pub_date', 'author']
 
 def __unicode__(self):
  return self.author.username + ": " + self.content[:64] + "..."

class Squealer(models.Model):
 user = models.ForeignKey(User, related_name="users")
 followers = models.ManyToManyField('self', blank=True)
 following = models.ManyToManyField('self', blank=True)

 def __unicode__(self):
  return (self.user.first_name or self.username) + " " + self.user.last_name
