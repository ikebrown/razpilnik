from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django.db.models import F, Q

from models import *
from forms import *

def index(request):
 template = loader.get_template('squeal/index.html')
 squeals = Squeal.objects.all()
 squealers = Squealer.objects.all()
 context = RequestContext(request, {"squeals": squeals, "squealers": squealers})
 if request.user.is_authenticated():
   return redirect(home)
 else:
   return HttpResponse(template.render(context))

def squeal(request, squealer, squeal_id):
  squeal = Squeal.objects.get(id=squeal_id)
  template = loader.get_template('squeal/squeal.html')
  context = RequestContext(request, { "squeal": squeal })
  return HttpResponse(template.render(context))

def squealer(request, squealer):
 template = loader.get_template('squeal/squealer.html')
 squealer = Squealer.objects.get(user__username=squealer)
 squeals = Squeal.objects.filter(author=squealer)
 context = RequestContext(request, {"squealer": squealer, "squeals": squeals})
 if squealer.user == request.user:
  form = SquealForm(request.POST)
  context["form"] = form
 return HttpResponse(template.render(context))

@login_required
def squeal_delete(request, squealer, squeal_id):
 if request.user.username != squealer: raise PermissionDenied
 template = loader.get_template("squeal/squeal_delete.html")
 squealer = Squealer.objects.get(user__username=squealer)
 squeal = Squeal.objects.get(id=squeal_id)
 if request.user != squeal.author.user: raise PermissionDenied
 if request.method == "POST":
  # User confirmed deletion
  squeal.delete()
  return redirect(home)
 context = RequestContext(request, {"squealer": squealer, "squeal": squeal})
 return HttpResponse(template.render(context))
 #template = 
 
@login_required
def settings(request, squealer):
 if request.user.username != squealer: raise PermissionDenied
 squealer = Squealer.objects.get(user__username=squealer)
 if request.method == "POST":
  form = SquealerForm(request.POST, squealer)
  if form.is_valid():
   pass
   # Save data
 else:
  form = SquealerForm(squealer)

 context = RequestContext(request, {"squealer": squealer, "form": form})
 template = loader.get_template('squeal/squealer_settings.html')
 return HttpResponse(template.render(context))

@login_required
def home(request):
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
  squeals = Squeal.objects.filter(Q(author__in=squealer.following.all()) | Q(author=squealer))
  context = RequestContext(request, {"squealer": squealer, "followers": followers, "squeals": squeals, "form": form})
  return HttpResponse(template.render(context)) 
