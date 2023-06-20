from django import forms
from .models import Post, Blok

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ("avtor",)

class BlokForm(forms.ModelForm):
    class Meta:
        model = Blok
        exclude = ("bloker",)
