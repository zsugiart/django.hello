# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# django stuff

from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from django.views import generic

# django forms

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# rest framework

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','email','password']


# define the views here


@login_required
def logout(request):
    """Log the current user out."""
    logout_user(request)
    return redirect('home')


class UserFormView(generic.View):
    form_class = UserForm
    template_name = "signup.html"

    # form is requested (GET)
    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form':form})

    # form is POSTed for processing
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # cleaned/normalized data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.username = username
            user.set_password(password)
            user.save()
            # after user record is added, authenticate the user
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('url>home')
        # else
        return render(request, self.template_name, {'form':form })
