from rest_framework import serializers

from .models import PlayList, Video


class PlayListSerializer(serializers.HyperlinkedModelSerializer):
    # video_set = serializers.HyperlinkedRelatedField(
    #    view_name="video_detail", many=True, queryset="video_set"
    # )

    class Meta:
        model = PlayList
        fields = (
            "url",
            "is_anonymous",
            "title",
            "public",
            "date",
            "token",
            "last_update",
            "last_get",
            "video_set",
        )
        extra_kwargs = {"url": {"lookup_field": "token"}}


class VideoSerializer(serializers.ModelSerializer):
    playlist = serializers.HyperlinkedRelatedField(
        view_name="playlist-detail",
        lookup_field="token",
        queryset=PlayList.objects.all(),
    )

    class Meta:
        model = Video
        fields = ("url", "playlist", "token", "title")
