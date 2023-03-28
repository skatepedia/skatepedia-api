from django_distill import distill_path

from django.urls import path
from django.views.generic import TemplateView
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap

from .views import (
    video_list,
    video_detail,
    get_all_video_slugs,
    get_all_videos_paged
)

urlpatterns = [
    distill_path(
        "videos/pages/<int:page>.html",
        video_list,
        name="archive-video-list",
        distill_func=get_all_videos_paged,
        distill_status_codes=(200, 404),
    ),
    distill_path(
        "videos/<slug:slug>.html",
        video_detail,
        name="archive-video-detail",
        distill_func=get_all_video_slugs,
        distill_status_codes=(200, 404),
    ),
]
