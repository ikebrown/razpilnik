from django.http import HttpResponse, Http404
from django.template import Context, loader
from models import *

def index(request):
 template = loader.get_template('squeal/index.html')
 squeals = Squeal.objects.all()
 squealers = Squealer.objects.all()
 context = Context({"squeals": squeals, "squealers": squealers})
 return HttpResponse(template.render(context))

def squealer(request, squealer):
 template = loader.get_template('squeal/squealer.html')
 squealer = Squealer.objects.get(user__username=squealer)
 squeals = Squeal.objects.filter(author=squealer.user)
 context = Context({"squealer": squealer, "squeals": squeals})
 return HttpResponse(template.render(context)) 
