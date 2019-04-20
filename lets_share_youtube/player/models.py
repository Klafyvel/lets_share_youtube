import random
import json

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

import requests


class PlayList(models.Model):
    """A PlayList, i.e. a collection of videos"""

    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    public = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    token = models.CharField(blank=True, null=False, unique=True, max_length=100)
    last_update = models.DateTimeField(auto_now=True)
    last_get = models.DateTimeField(auto_now=True)

    def __str__(self):
        return u"Playlist " + str(self.token)

    def create_token(self):
        """Creates a token for the playlist if it hasn't been done yet."""
        if not self.token:
            self.token = str(
                int(timezone.now().timestamp()) << settings.RANDOM_LENGTH
                | random.randint(0, 2 ** settings.RANDOM_LENGTH - 1)
            )

    def save(self, *args, **kwargs):
        self.create_token()
        super().save(*args, **kwargs)

    @property
    def is_anonymous(self):
        return self.owner is None


class Video(models.Model):
    """Represents a YouTube video."""

    playlist = models.ForeignKey(PlayList, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    title = models.CharField(blank=True, max_length=100)

    def __str__(self):
        return u"Link : " + self.token + u" of " + str(self.playlist)

    def save(self, *args, **kwargs):
        self.update_title()
        super().save(*args, **kwargs)

    @property
    def owner(self):
        return self.playlist.owner

    @property
    def public(self):
        return self.playlist.public

    def update_title(self):
        """Fetch the title of the video on YouTube using its token."""
        response = requests.get(settings.YOUTUBE_INFO_URL.format(self.token))
        self.title = json.loads(response.content.decode("utf-8"))["title"]
