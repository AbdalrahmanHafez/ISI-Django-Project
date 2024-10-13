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
from officers_affairs import models, views
from django.http import HttpResponse
import json

import cv2
from rembg import remove
import numpy as np
import os


def remove_bk(input_image_path, output_image_path):
    # try:
    input_image = cv2.imread(input_image_path)

    with open(input_image_path, 'rb') as input_file:
        image_data = input_file.read()
        result = remove(image_data)

    np_result = np.frombuffer(result, np.uint8)
    img_no_bg = cv2.imdecode(np_result, cv2.IMREAD_UNCHANGED)

    height, width = img_no_bg.shape[:2]
    white_background = np.ones((height, width, 3), dtype=np.uint8) * 255

    if img_no_bg.shape[2] == 4:
        alpha_channel = img_no_bg[:, :, 3]
        rgb_img = img_no_bg[:, :, :3]
        alpha_mask = alpha_channel / 255.0

        for c in range(3):
            white_background[:, :, c] = (alpha_mask * rgb_img[:, :, c] +
                                            (1 - alpha_mask) * white_background[:, :, c])
    else:
        white_background = img_no_bg

    cv2.imwrite(output_image_path, white_background)
    print(f"Output saved successfully at {output_image_path}")
    
    # except Exception as e:
    #     print(f"Error: {e}")

def testView(request):
    error = 1/0

    return render(request, "test.html")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('test/', testView),
    path('officers_affairs/', include('officers_affairs.urls')),
    path('', RedirectView.as_view(url=reverse_lazy("home"))),
    path('about/', views.about, name='about'),
    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

