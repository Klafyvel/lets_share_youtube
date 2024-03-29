from django.urls import path
from . import views

app_name = "player"
urlpatterns = [
    path("", views.index, name="index"),
    path("p/<str:token>", views.playlist, name="playlist"),
]
