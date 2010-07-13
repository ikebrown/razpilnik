# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django.db.models import F, Q
from django.core.files.base import ContentFile
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from PIL import Image

from models import *
from forms import *

def index(request, page=1):
 template = loader.get_template('squeal/index.html')
 paginator = Paginator(Squeal.objects.all(), 8)
 try:
  squeals = paginator.page(page)
 except (EmptyPage, InvalidPage):
  squeals = paginator.page(paginator.num_pages)

 squealers = Squealer.objects.all()[:24]
 context = RequestContext(request, {"squeals": squeals, "squealers": squealers, "page": page})
 if request.user.is_authenticated():
   return redirect(home)
 else:
   return HttpResponse(template.render(context))

def squeal(request, squealer, squeal_id):
  squealer = get_object_or_404(Squealer, user__username=squealer)
  squeal = get_object_or_404(Squeal, id=squeal_id)
  template = loader.get_template('squeal/squeal.html')
  context = RequestContext(request, { "squeal": squeal })
  return HttpResponse(template.render(context))

def squealer(request, squealer, page=1):
 template = loader.get_template('squeal/squealer.html')
 squealer = get_object_or_404(Squealer, user__username=squealer)
 followers = Squealer.objects.filter(following=squealer)
 squeals = Squeal.objects.filter(author=squealer)
 paginator = Paginator(squeals, 8)
 try:
  squeals = paginator.page(page)
 except (EmptyPage, InvalidPage):
  squeals = paginator.page(paginator.num_pages)

 context = RequestContext(request, {"squealer": squealer, "squeals": squeals, "followers": followers, "page": page})
 if squealer.user == request.user:
  form = SquealForm(request.POST)
  context["form"] = form
 return HttpResponse(template.render(context))

@login_required
def squeal_delete(request, squealer, squeal_id):
 if request.user.username != squealer: raise PermissionDenied
 template = loader.get_template("squeal/squeal_delete.html")
 squealer = get_object_or_404(Squealer, user__username=squealer)
 squeal = get_object_or_404(Squeal, id=squeal_id)
 if request.user != squeal.author.user: raise PermissionDenied
 if request.method == "POST":
  # User confirmed deletion
  squeal.delete()
  return redirect(home)
 context = RequestContext(request, {"squealer": squealer, "squeal": squeal})
 return HttpResponse(template.render(context))

@login_required
def follow(request, to_follow):
 to_follow = get_object_or_404(Squealer, user__username=to_follow)
 follower = Squealer.objects.get(user=request.user)
 followers = Squealer.objects.filter(following=to_follow)
 squeals = Squeal.objects.filter(author=to_follow)
 template = loader.get_template("squeal/follow.html")
 if to_follow in follower.following.all():
  return redirect('razpilnik.squeal.views.squealer', squealer=to_follow.user.username)
 if request.method == "POST":
  follower.following.add(to_follow)
  return redirect('razpilnik.squeal.views.squealer', squealer=to_follow.user.username)
 context = RequestContext(request, {"squealer": to_follow, "squeals": squeals, "followers": followers})
 return HttpResponse(template.render(context))
 
@login_required
def unfollow(request, to_follow):
 to_follow = get_object_or_404(Squealer, user__username=to_follow)
 follower = Squealer.objects.get(user=request.user)
 followers = Squealer.objects.filter(following=to_follow)
 squeals = Squeal.objects.filter(author=to_follow)
 template = loader.get_template("squeal/unfollow.html")
 if to_follow not in follower.following.all():
  return redirect('razpilnik.squeal.views.squealer', squealer=to_follow.user.username)
 if request.method == "POST":
  follower.following.remove(to_follow)
  return redirect('razpilnik.squeal.views.squealer', squealer=to_follow.user.username)
 context = RequestContext(request, {"squealer": to_follow, "squeals": squeals, "followers": followers})
 return HttpResponse(template.render(context))
 
@login_required
def settings(request):
 squealer = request.user.get_profile()
 if request.method == "POST":
  form = SquealerForm(request.POST, request.FILES, instance=squealer)
  if form.is_valid():
   squealer = form.save()
 else:
  form = SquealerForm(instance=squealer)

 context = RequestContext(request, {"squealer": squealer, "form": form})
 template = loader.get_template('squeal/squealer_settings.html')
 return HttpResponse(template.render(context))

@login_required
def home(request, page=1):
 squealer = Squealer.objects.get(user=request.user)
 if request.method == "POST":
   form = SquealForm(request.POST)
   if form.is_valid():
     newsqueal = Squeal(content=form.cleaned_data["content"], author=squealer)
     newsqueal.save()
     # Reset form
     form = SquealForm()
 else:
   form = SquealForm()

 template = loader.get_template('squeal/home.html')
 followers = Squealer.objects.filter(following=squealer)
 squeals = Squeal.objects.filter(author__in=squealer.following.all()) | Squeal.objects.filter(author=squealer)
 paginator = Paginator(squeals, 8)
 try:
  squeals = paginator.page(page)
 except (EmptyPage, InvalidPage):
  squeals = paginator.page(paginator.num_pages)

 context = RequestContext(request, {"squealer": squealer, "followers": followers, "squeals": squeals, "form": form})
 return HttpResponse(template.render(context)) 
