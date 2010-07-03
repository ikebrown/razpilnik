from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from models import *
from forms import *

def index(request):
 template = loader.get_template('squeal/index.html')
 squeals = Squeal.objects.all()
 squealers = Squealer.objects.all()
 context = RequestContext(request, {"squeals": squeals, "squealers": squealers})
 return HttpResponse(template.render(context))

def squealer(request, squealer):
 template = loader.get_template('squeal/squealer.html')
 squealer = Squealer.objects.get(user__username=squealer)
 squeals = Squeal.objects.filter(author=squealer.user)
 context = RequestContext(request, {"squealer": squealer, "squeals": squeals})
 return HttpResponse(template.render(context))
 
@login_required
def settings(request, squealer):
 if request.user.username != squealer: raise PermissionDenied
 squealer = get_object_or_404(Squealer, user__username=squealer)
 form = SquealerForm(request.POST, squealer)
 context = RequestContext(request, {"squealer": squealer, "form": form})
 template = loader.get_template('squeal/squealer_settings.html')
 return HttpResponse(template.render(context))

@login_required
def home(request):
   return HttpResponse("Welcome home, " + request.user.username) 