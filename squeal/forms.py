from django.forms import ModelForm
from models import Squealer


class SquealerForm(ModelForm):
  class Meta:
    model = Squealer
    fields = ('location', 'bio', 'website', 'followers')