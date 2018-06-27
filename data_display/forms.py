from django import forms
from . import models

class changeForm(forms.ModelForm):
    
    class Meta:
        model = models.change
        fields = ['attributeName','oldValue','newValue']
