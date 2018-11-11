"""Skatepedia URL Configuration"""
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.urls import path, include
from django.conf import settings


urlpatterns = [
    path('', RedirectView.as_view(url=settings.SKATEPEDIA_API_V1_URL)),
    path('admin/', admin.site.urls),
    path(settings.SKATEPEDIA_API_V1_URL,
         include('skatepedia.api.urls', namespace='api'))
]
