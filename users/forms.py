from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import CustomUser

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django import forms
from home.models import Comments
from django.contrib.auth.models import User

class CustomPasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Eski parol")
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Yangi parol")
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Yangi parol (takroran)")

class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['avatar_image']

class CommentForm(forms.ModelForm):
    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1 dan 5 gacha'})
    )
    text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Sharhingizni kiriting...'})
    )

    class Meta:
        model = Comments
        fields = ['text', 'rating']