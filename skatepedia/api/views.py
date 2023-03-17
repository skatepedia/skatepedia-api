import django_filters.rest_framework
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


class SkaterViewSet(viewsets.ModelViewSet):
    queryset = Skater.objects.all()
    serializer_class = SkaterSerializer


class FilmmakerViewSet(viewsets.ModelViewSet):
    queryset = Filmmaker.objects.all()
    serializer_class = FilmmakerSerializer


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ["year", "runtime", "company", "skaters", "filmmakers"]


class VideoCategoryViewSet(viewsets.ModelViewSet):
    queryset = VideoCategory.objects.all()
    serializer_class = VideoCategorySerializer


class ClipViewSet(viewsets.ModelViewSet):
    queryset = Clip.objects.all()
    serializer_class = ClipSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class SoundtrackViewSet(viewsets.ModelViewSet):
    queryset = Soundtrack.objects.all()
    serializer_class = SoundtrackSerializer


class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
