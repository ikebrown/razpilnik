from django import forms
from models import *

class SquealForm(forms.Form):
  content = forms.CharField(max_length=140, widget=forms.Textarea)
class SquealerForm(forms.ModelForm):
  class Meta:
    model = Squealer
    fields = ('location', 'bio', 'website', 'followers')