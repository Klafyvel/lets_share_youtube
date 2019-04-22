from django.shortcuts import render


def index(request):
    return render(request, "ui/index.html")


def playlist(request, token):
    return render(request, "ui/playlist.html")
