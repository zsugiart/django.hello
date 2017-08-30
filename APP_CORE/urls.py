"""APP_CORE URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include,url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views
from Hello import views as hello_views

urlpatterns = [

    # no name needed. use admin:index
    url(r'^admin/', include(admin.site.urls) ),

    # for default template location - see APP_CORE
    url(r'^account/login/$', auth_views.login, {'template_name': 'login.html'},     name="url>login"),
    url(r'^account/logout/$', auth_views.logout, {'next_page': '/account/login/'},  name="url>logout"),
    url(r'^account/signup/$', views.UserFormView.as_view(), name="url>signup"),

    # point project root / to ...
    # Hello.urls
    url(r'^$', hello_views.home,           name="url>home"),

    # app1. Hello
    # map hello/ to Hello.urls
    url(r'^hello/', include('Hello.urls')),

    # --- add other app here ----

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
