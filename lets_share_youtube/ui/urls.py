from django.urls import path
from . import views

app_name = "player"
urlpatterns = [
    path("", views.index, name="index"),
    path("playlist/<str:token>", views.playlist, name="playlist"),
]
