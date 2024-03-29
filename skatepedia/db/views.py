from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sitemaps import Sitemap
from django.template.response import TemplateResponse

from skatepedia.db.models import Video

DEFAULT_PAGE_SIZE = 25


class VideoSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Video.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


def video_list(request):
    page = request.GET.get("page", 1)
    videos = Video.objects.all().values_list("slug", "title", named=True)
    paginator = Paginator(videos, DEFAULT_PAGE_SIZE)
    page_obj = paginator.get_page(page)
    return TemplateResponse(request, "db/video_list.html", {"page_obj": page_obj})


def video_detail(request, slug):
    video = Video.objects.filter(slug=slug).first()
    # Have an static HTML on IPFS
    if video and video.archive_file:
        return HttpResponse(
            video.archive_file.read(),
            headers={"x-ipfs-path": video.archive_file.url},
        )

    return (
        TemplateResponse(request, "db/video_detail.html", {"video": video})
        if video
        else HttpResponseNotFound("Video not found")
    )


def get_all_videos():
    return Video.objects.all()
