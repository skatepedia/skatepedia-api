from rest_framework_json_api import serializers

from skatepedia.db.models import (
    Clip,
    Track,
    Video,
    Skater,
    Company,
    BaseModel,
    Filmmaker,
    Soundtrack,
    VideoCategory
)


def nested_resource(_model, _fields="__all__", _exclude=None, _depth=0):
    class NestedSerializer(serializers.ModelSerializer):
        class Meta:
            model = _model
            depth = _depth
            fields = _fields
            exclude = _exclude

    return NestedSerializer


class SoundtrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Soundtrack
        exclude = ("skatevideosite_id", "raw_data", "updated_by")


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ("name", "artist", "links")


class SkaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skater
        exclude = ("skatevideosite_id", "raw_data", "updated_by")


class FilmmakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filmmaker
        exclude = ("skatevideosite_id", "raw_data", "updated_by")


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ("skatevideosite_id", "raw_data", "updated_by")
        model = Video


class VideoCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoCategory
        exclude = ("skatevideosite_id", "raw_data", "updated_by")


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        exclude = ("skatevideosite_id", "raw_data", "updated_by")


class ClipSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True)
    # TODO:review
    skaters = nested_resource(Skater, _fields=("id", "name"))(many=True)

    class Meta:
        model = Clip
        exclude = ("skatevideosite_id", "raw_data", "updated_by")
