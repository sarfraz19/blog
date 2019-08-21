from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.contrib.auth.models import User


class PostForm(forms.Form):
    title = forms.CharField(max_length=250)
    content = forms.Textarea()