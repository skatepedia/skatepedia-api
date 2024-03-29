"""Skatepedia URL Configuration"""
from django.conf import settings
from django.urls import path, include
from django.contrib import admin
from django.views.generic.base import RedirectView

from skatepedia.db import urls as website_urls
from skatepedia.archive import urls as archive_urls

urlpatterns = [
    path("", RedirectView.as_view(url=settings.SKATEPEDIA_API_V1_URL)),
    path("", include(website_urls)),
    path("", include(archive_urls)),
    path("admin/", admin.site.urls),
    # path(f"{settings.SKATEPEDIA_API_V1_URL}auth/",
    #      include("rest_framework.urls", namespace="rest_framework")),
    path(
        settings.SKATEPEDIA_API_V1_URL, include("skatepedia.api.urls", namespace="api")
    ),
]
