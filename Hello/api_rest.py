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

class HelloList(APIView):
    def get(self, request):
        recs = Hello.objects.all()
        serializer = HelloSerializer(recs,many=True)
        return Response(serializer.data)


    def post(self):
        pass
