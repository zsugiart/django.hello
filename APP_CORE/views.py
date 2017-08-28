# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# django stuff

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

# django forms

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# rest framework

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# define the views here

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login(request):
    """Attempt to log a user in."""
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login_user(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'form.html', {
        'title':       'Login',
        'form':        form,
        'form_action': 'Login',
    })

@login_required
def logout(request):
    """Log the current user out."""
    logout_user(request)
    return redirect('home')
