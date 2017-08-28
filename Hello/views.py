# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# django stuff

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required

# rest framework

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# app

from .models import *

# define the views here

def home(request):
    # where we share data between backend and view
    context = {
    }
    return render(
        request=request,
        template_name='home.html',
        context=context)


@login_required
def index(request):
    # get all hellos from the DB
    all_hello = Hello.objects.all()
    # where we share data between backend and view
    context = {
        'list_hello' : all_hello,
    }
    # or for shortcut, you can also do:
    return render(
        request=request,
        template_name='index.html',  # searches in App/templates/*
        context=context)

@login_required
def detail(request, id):
    rec = Hello.objects.get(pk=id)
    context = { 'hello' : rec }
    return render(
        request=request,
        template_name='detail.html',
        context=context
    )
