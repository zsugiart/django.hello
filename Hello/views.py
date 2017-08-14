# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers

# rest framework

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# app

from .models import *

# Create your views here.

def index(request):
    html = '<h1>HELLO WORLD</h1>'
    all_hello = Hello.objects.all()
    for hello in all_hello:
        html += "<a href='./%s'>%s</a> <br />" % ( hello.id, hello.label )
    return HttpResponse(html)

def detail(request, id):
    html = "<H1>ID="+id+"</H1>"
    rec = Hello.objects.get(pk=id)
    html += "<br/>label:"+rec.label
    html += "<br/>desc:"+rec.desc
    html += "<br/>last update: "+rec.date_u.__str__()
    return HttpResponse(html)
