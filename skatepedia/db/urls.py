from django.urls import path

from .views import home, video_detailc

urlpatterns = [
    path("", home, name="home"),
    path("videos/<slug:slug>/", video_detail, name="video-detail"),
]
