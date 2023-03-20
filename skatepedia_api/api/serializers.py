from rest_framework import serializers

from skatepedia_db.db.models import (
    Clip,
    Track,
    Video,
    Skater,
    Company,
    Filmmaker,
    Soundtrack,
    VideoCategory
)


class SkaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skater
        fields = "__all__"


class FilmmakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filmmaker
        fields = "__all__"


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = "__all__"


class VideoCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoCategory
        fields = "__all__"


class ClipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clip
        fields = "__all__"


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class SoundtrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Soundtrack
        fields = "__all__"


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = "__all__"
