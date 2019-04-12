from rest_framework import viewsets

from .models import PlayList, Video
from .serializers import PlayListSerializer, VideoSerializer


class PlayListViewSet(viewsets.ModelViewSet):
    """API endpoint that allows PlayLists to be viewed or edited."""

    queryset = PlayList.objects.all()
    serializer_class = PlayListSerializer
    lookup_field = "token"
    lookup_value_regex = "\w+"


class VideoViewSet(viewsets.ModelViewSet):
    """API endpoint that allows PlayLists to be viewed or edited."""

    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def get_queryset(self):
        return Video.objects.filter(playlist__token=self.kwargs["playlist_token"])
