from django_distill import distill_path

from django.urls import path

from .views import home, get_videos, video_detail

urlpatterns = [
    path("", home, name="home"),
    distill_path(
        "videos/<slug:slug>/",
        video_detail,
        name="video-detail",
        distill_func=get_videos,
        distill_status_codes=(200, 404),
    ),
]
