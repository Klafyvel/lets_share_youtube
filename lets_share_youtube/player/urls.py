from django.urls import include, path
from rest_framework_nested import routers

from . import views

router = routers.SimpleRouter()
router.register(r"playlists", views.PlayListViewSet)
video_router = routers.NestedSimpleRouter(router, r"playlists", lookup="playlist")

video_router.register(r"videos", views.VideoViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [path("", include(router.urls)), path("", include(video_router.urls))]
