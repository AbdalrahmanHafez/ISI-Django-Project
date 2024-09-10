"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include, reverse_lazy
from django.views.generic import TemplateView
from django.shortcuts import render
from django.forms import ModelForm
from django.conf.urls.static import static
from myproject import settings
from django.views.generic import CreateView, RedirectView
from officers_affairs import models
from django.http import HttpResponse
import json

def testView(request):
    return render(request, "test.html")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('test/', testView),
    path('officers_affairs/', include('officers_affairs.urls')),
    path('', RedirectView.as_view(url=reverse_lazy("home")))
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

