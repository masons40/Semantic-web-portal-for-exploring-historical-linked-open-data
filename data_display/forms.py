from django import forms
from . import models

class changeForm(forms.ModelForm):
    
    class Meta:
        model = models.changes
        fields = ['targetUri','attributeName','oldValue','newValue','userId']