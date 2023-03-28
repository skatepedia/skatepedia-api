from django_distill import distill_path

from django.urls import path
from django.views.generic import TemplateView
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap

from .views import (
    get_videos,
    video_list,
    video_detail,
    get_all_videos,
    get_video_pages
)

urlpatterns = [
    path(
        "robots.txt",
        TemplateView.as_view(template_name="db/robots.txt", content_type="text/plain"),
    ),
    path(
        "sitemap.xml",
        sitemap,
        {
            "sitemaps": {
                "videos": GenericSitemap({"queryset": get_all_videos()}, priority=0.6)
            }
        },
        name="django.contrib.sitemaps.views.sitemap",
    ),
    distill_path(
        "videos/pages/<int:page>.html",
        video_list,
        name="video-list",
        distill_func=get_video_pages,
        distill_status_codes=(200, 404),
    ),
    distill_path(
        "videos/<slug:slug>.html",
        video_detail,
        name="video-detail",
        distill_func=get_videos,
        distill_status_codes=(200, 404),
    ),
]
