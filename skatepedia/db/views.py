from django.http import HttpResponse, HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist
from django.template.response import TemplateResponse

from skatepedia.db.models import Video


def home(request):
    return TemplateResponse(request, "db/index.html")


def video_detail(request, slug):
    if video := Video.objects.filter(slug=slug).first():
        return HttpResponse(
            video.archive_file.read(),
            headers={
                "x-ipfs-path": video.archive_file.name  # TODO: return a valid dnslink
            },
        )
    return HttpResponseNotFound("Video not found")
