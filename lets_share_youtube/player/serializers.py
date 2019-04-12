from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from .models import PlayList, Video


class PlayListSerializer(serializers.HyperlinkedModelSerializer):

    video_set = NestedHyperlinkedRelatedField(
        view_name="video-detail",
        lookup_url_kwarg="playlist_token",
        read_only=True,
        many=True,
        parent_lookup_kwargs={"pk": "pk", "playlist_token": "playlist__token"},
    )

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


class VideoSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {"playlist_token": "playlist__token"}
    playlist = serializers.HyperlinkedRelatedField(
        view_name="playlist-detail",
        lookup_field="token",
        queryset=PlayList.objects.all(),
    )

    class Meta:
        model = Video
        fields = ("url", "playlist", "token", "title")
