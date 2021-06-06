from django import forms
from .models import *



class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput)

class AddKey(forms.ModelForm):
    class Meta:
        model=Key
        fields = ['type','host','port','user','password']

class ChangeKey(forms.ModelForm):
    class Meta:
        model=Key
        fields = ['type','host','port','user','password']


