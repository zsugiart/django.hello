# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# rest framework
from rest_framework import serializers

# Create your models here.

class Hello(models.Model):

    label = models.CharField(max_length=200)

    desc  = models.CharField(max_length=200)

    # set automatic creation date
    date_c = models.DateTimeField(auto_now_add=True)

    # set automatic update date
    date_u = models.DateTimeField(auto_now=True)

    # boolean field
    isGood = models.BooleanField(default=False)

    def dict(self):
        return dict(
            label=self.label.__str__(),  # convert into byte str
            desc=self.desc.__str__(),
            date_c=self.date_c,
            date_u=self.date_u,
            isGood=self.isGood
        )

class HelloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hello
        fields = ('label','date_c')
        #fields = '__all__'
