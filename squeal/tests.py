"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""
import unittest
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse

from razpilnik.squeal.models import *
from razpilnik.squeal.views import *

class BaseTest(TestCase):
 def user_test(self):
  
  ''' 
    TODO: 
     Auth test: register, login, activation
     Squeal test: post, delete
     Follow test: follow, unfollow
     View tests
  '''
 def test_public_views(self):
  user = User(username="crash", password="test", email="crasher@test.com")
  user.save()
  user1 = User(username="bug", password="test", email="crasher@test.com")
  user1.save()

  squealer = Squealer(user=user)
  squealer.save()

  squealer1 = Squealer(user=user1)
  squealer1.save()

  squeal = Squeal(author=squealer, content="Testing and crashing...")
  squeal.save()

  index = self.client.get("/")
  login = self.client.get("/accounts/login")
  register = self.client.get("/accounts/register")
  squeal = self.client.get("/"+squealer.user.username+"/squeal/"+str(squeal.id), {})
  squealer = self.client.get("/"+squealer.user.username+"/", {})

  self.assertTrue(index.status_code < 400) 
  self.assertTrue(login.status_code < 400) 
  self.assertTrue(register.status_code < 400) 
  self.assertTrue(squeal.status_code < 400) 
  self.assertTrue(squealer.status_code < 400) 

 def test_private_views(self):
  login = self.client.post("/accounts/login", {"username": "crash", "password": "test"}) 
  self.assertTrue(login.status_code < 400) 

  home = self.client.get("/home")
  self.assertTrue(home.status_code < 400) 

  settings = self.client.get("/accounts/settings")
  self.assertTrue(settings.status_code < 400) 

  follow = self.client.get("/follow/bug")
  self.assertTrue(follow.status_code < 400) 

  unfollow = self.client.get("/unfollow/bug")
  self.assertTrue(unfollow.status_code < 400) 

