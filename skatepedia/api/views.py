from rest_framework import viewsets

from skatepedia.db.models import (
    Clip,
    Track,
    Video,
    Skater,
    Company,
    Filmmaker,
    Soundtrack
)
from skatepedia.api.serializers import *


class SkaterViewSet(viewsets.ReadOnlyModelViewSet):
    resource_name = "skaters"
    queryset = Skater.objects.all()
    serializer_class = SkaterSerializer
    filterset_fields = ["gender", "city", "stance"]


class FilmmakerViewSet(viewsets.ReadOnlyModelViewSet):
    resource_name = "filmmakers"
    queryset = Filmmaker.objects.all()
    serializer_class = FilmmakerSerializer


class VideoViewSet(viewsets.ReadOnlyModelViewSet):
    resource_name = "videos"
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    filterset_fields = {
        "year": ("exact", "lt", "gt", "lte", "gte", "in"),
        "runtime": ("exact", "lt", "gt", "lte", "gte", "in"),
    }


class VideoCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    resource_name = "video-categories"
    queryset = VideoCategory.objects.all()
    serializer_class = VideoCategorySerializer


class ClipViewSet(viewsets.ReadOnlyModelViewSet):
    resource_name = "clips"
    queryset = Clip.objects.all()
    serializer_class = ClipSerializer

    # def get_queryset(self):
    #     video = self.request.query_params.get('video')
    #     if video is None:
    #         return Clip.objects.none()
    #     return Clip.objects.filter(video__pk=video).prefetch_related('tracks')


class CompanyViewSet(viewsets.ReadOnlyModelViewSet):
    resource_name = "companies"
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class SoundtrackViewSet(viewsets.ReadOnlyModelViewSet):
    resource_name = "soundtracks"
    queryset = Soundtrack.objects.all()
    serializer_class = SoundtrackSerializer


class TrackViewSet(viewsets.ReadOnlyModelViewSet):
    resource_name = "tracks"
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
