from django_distill import distill_path

from django.urls import path

from .views import get_videos, video_list, video_detail, get_video_pages

urlpatterns = [
    distill_path(
        "videos/pages/<int:page>/",
        video_list,
        name="video-list",
        distill_func=get_video_pages,
        distill_status_codes=(200, 404),
    ),
    distill_path(
        "videos/<slug:slug>/",
        video_detail,
        name="video-detail",
        distill_func=get_videos,
        distill_status_codes=(200, 404),
    ),
]
