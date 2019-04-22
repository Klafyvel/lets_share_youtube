from urllib.parse import urlparse, parse_qs

from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action

from .permissions import IsOwnerOrPublic
from .models import PlayList, Video
from .serializers import PlayListSerializer, VideoSerializer


class PlayListViewSet(viewsets.ModelViewSet):
    """API endpoint that allows PlayLists to be viewed or edited."""

    # queryset = PlayList.objects.all()
    serializer_class = PlayListSerializer
    lookup_field = "token"
    lookup_value_regex = "\w+"
    permission_classes = [IsOwnerOrPublic]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return PlayList.objects.filter(owner=user) | PlayList.objects.filter(
                public=True
            )
        else:
            return PlayList.objects.filter(public=True)


class VideoViewSet(viewsets.ModelViewSet):
    """API endpoint that allows PlayLists to be viewed or edited."""

    # queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsOwnerOrPublic]

    def get_queryset(self):
        return Video.objects.filter(
            playlist__token=self.kwargs["playlist_token"]
        ).order_by("index")

    @action(detail=False, methods=["post"])
    def from_url(self, request, playlist_token):
        p = urlparse(request.data["url"])
        p = parse_qs(p.query)
        playlist = get_object_or_404(PlayList, token=playlist_token)
        try:
            v = Video.objects.create(playlist=playlist, token=p["v"][0])
            return Response(
                {
                    "status": "created",
                    "url": self.reverse_action(
                        "detail", kwargs={"playlist_token": playlist_token, "pk": v.pk}
                    ),
                }
            )
        except KeyError:
            return Response({"status": "failed"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def up(self, request, playlist_token, pk):
        video = get_object_or_404(Video, pk=pk)
        video.up_index()
        return Response({"status": "upgraded"})

    @action(detail=True, methods=["post"])
    def down(self, request, playlist_token, pk):
        video = get_object_or_404(Video, pk=pk)
        print(video)
        video.down_index()
        return Response({"status": "downgraded"})
