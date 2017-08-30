from django.conf.urls import url
from . import views
from . import api_rest
from . import api_rpc

# rest framework
from rest_framework.urlpatterns import format_suffix_patterns

# rpc

from modernrpc.views import RPCEntryPoint

# /hello
urlpatterns = [

# ** VIEWS **
# /v/*
    url(r'^$', views.index,                     name='url>hello'),
    url(r'^(?P<id>[0-9]+)/$', views.detail,     name='url>hello.detail'),

# ** API **
# /api/rest/* (JSON RESTFUL)
# /api/rpc/*  (XML/JSON RPC)

    url(r'^api/rest/', api_rest.HelloList.as_view(), name = "url>hello.api.rest"),
    url(r'^api/rpc/', RPCEntryPoint.as_view(),       name = "url>hello.api.rpc"),

]

# for rest framework
urlpatterns = format_suffix_patterns(urlpatterns)
