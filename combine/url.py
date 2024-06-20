"""safetymap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from os import name
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.shortcuts import render
from django.http import HttpResponse
from . import views

def set_spot_view(request):
    return HttpResponse("SetSpot view function")
urlpatterns = [
   path('',views.home, name='home'),
   path('path',views.PathFinder, name='pathfinder'),
   path('SetSpot', views.GetSpotPoint, name='getspotpoint'),
   path('saferoute',views.saferoute, name='saferoute'),
   path('SetSpot/', views.set_spot_view, name='SetSpot'),
   path('recognize_speech/', views.start_speech_recognition, name='recognize_speech'),
   path('detect_scream/', views.start_scream_detection, name='detect_scream'),

]
