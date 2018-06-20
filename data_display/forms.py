from django import forms


class changeForm(forms.Form):
    attributeName = forms.CharField(max_length=300)
    oldValue = forms.CharField(max_length=300)
    newValue = forms.CharField(max_length=300)
