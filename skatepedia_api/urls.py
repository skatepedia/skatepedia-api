"""Skatepedia URL Configuration"""
from django.conf import settings
from django.urls import path, include
from django.contrib import admin
from django.views.generic.base import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url=settings.SKATEPEDIA_API_V1_URL)),
    path("admin/", admin.site.urls),
    # path(f"{settings.SKATEPEDIA_API_V1_URL}auth/",
    #      include("rest_framework.urls", namespace="rest_framework")),
    path(
        settings.SKATEPEDIA_API_V1_URL,
        include("skatepedia_api.api.urls", namespace="api"),
    ),
]
