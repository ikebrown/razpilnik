from django.http import HttpResponse, Http404
from django.template import Context, loader
from forms import *

def login(request):
 if request.method == 'POST':
  form = LoginForm(request.POST)
  context = Context({"form": form})
  template = loader.get_template("login/index.html")
  if form.is_valid(): return HttpResponse("Success")
  else: return HttpResponse(template.render(context))
 else:
   form = LoginForm()
   context = Context({"form": form})
   template = loader.get_template("login/index.html")
   return HttpResponse(template.render(context))
def logout(request):
 return HttpResponse()
def signup(request): 
 return HttpResponse()
