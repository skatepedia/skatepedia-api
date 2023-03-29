from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.template.response import TemplateResponse

from skatepedia.db.models import Video

DEFAULT_PAGE_SIZE = 25


def video_list(request, page):
    videos = Video.objects.all().values_list("slug", "title", named=True)
    paginator = Paginator(videos, DEFAULT_PAGE_SIZE)
    page_obj = paginator.get_page(page)
    return TemplateResponse(request, "archive/video_list.html", {"page_obj": page_obj})


def video_detail(request, slug):
    video = Video.objects.filter(slug=slug).first()
    # Have an static HTML on IPFS
    if video and video.archive_file:
        return HttpResponse(
            video.archive_file.read(),
            headers={"x-ipfs-path": video.archive_file.url},
        )

    return (
        TemplateResponse(request, "archive/video_detail.html", {"video": video})
        if video
        else HttpResponseNotFound("Video not found")
    )


def get_all_videos_qs():
    return Video.objects.all()


def get_all_video_slugs():
    for video in Video.objects.all().values_list("slug")[:5]:
        yield video


def get_all_videos_paged():
    videos_qs = Video.objects.all().values_list("pk", flat=True).order_by("created_at")
    paged = Paginator(videos_qs, DEFAULT_PAGE_SIZE)
    for page in paged.page_range:
        yield [page]
