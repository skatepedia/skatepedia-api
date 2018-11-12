from rest_framework import serializers

from skatepedia.db.models import (
    Skater,
    Person,
    Company,
    Video,
    Clip,
    Soundtrack,
    Track,
)


class SkaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skater
        fields = '__all__'


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'


class ClipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clip
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class SoundtrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Soundtrack
        fields = '__all__'

class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = '__all__'
