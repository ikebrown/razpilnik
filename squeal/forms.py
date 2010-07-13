# -*- coding: utf-8 -*-
from django import forms
from django.forms.formsets import formset_factory
from django.contrib.auth.forms import *

from models import *

class SquealForm(forms.Form):
  content = forms.CharField(max_length=140, widget=forms.Textarea)

class SquealerForm(forms.ModelForm):
  class Meta:
    model = Squealer
    exclude  = ('user', 'following')

