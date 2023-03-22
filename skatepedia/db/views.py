from django.http import HttpResponse, HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist
from django.template.response import TemplateResponse

from skatepedia.db.models import Video


def home(request):
    return TemplateResponse(request, "db/index.html")


def video_detail(request, slug):
    video = Video.objects.filter(slug=slug).first()
    if video and video.archive_file:
        return HttpResponse(
            video.archive_file.read(),
            headers={
                "x-ipfs-path": video.archive_file.name  # TODO: return a valid dnslink
            },
        )
    return HttpResponseNotFound("Video not found")


def get_videos():
    return Video.objects.all().values_list("slug").iterator()
