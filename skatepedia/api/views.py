from rest_framework import viewsets

from skatepedia.db.models import (
    Skater,
    Person,
    Brand,
    Video,
    Clip,
    Soundtrack,
    Track,
)
from skatepedia.api.serializers import *


class SkaterViewSet(viewsets.ModelViewSet):
    queryset = Skater.objects.all()
    serializer_class = SkaterSerializer


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class ClipViewSet(viewsets.ModelViewSet):
    queryset = Clip.objects.all()
    serializer_class = ClipSerializer


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class SoundtrackViewSet(viewsets.ModelViewSet):
    queryset = Soundtrack.objects.all()
    serializer_class = SoundtrackSerializer


class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
