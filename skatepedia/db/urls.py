from django_distill import distill_path

from django.urls import path
from django.views.generic import TemplateView
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap

from .views import VideoSitemap, video_list, video_detail, get_all_videos

urlpatterns = [
    path(
        "robots.txt",
        TemplateView.as_view(template_name="db/robots.txt", content_type="text/plain"),
    ),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": {"videos": VideoSitemap}},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path(
        "videos",
        video_list,
        name="video-list",
    ),
    path(
        "videos/<str:slug>",
        video_detail,
        name="video-detail",
    ),
]
