from django.test import TestCase

from .models import PlayList, Video


class PlayListTestCase(TestCase):
    """Tests for PlayList."""

    def setUp(self):
        PlayList.objects.create(title="Test playlist")

    def test_token_already_created(self):
        """A token should be added if, and only if, no one has been set before."""
        already_created = PlayList.objects.get(title="Test playlist")
        token = "plop"
        already_created.token = token
        already_created.save()
        already_created = PlayList.objects.get(title="Test playlist")
        self.assertEqual(already_created.token, token)

    def test_token_not_set(self):
        """A token should be added if, and only if, no one has been set before."""
        playlist = PlayList.objects.create(title="Another test playlist")
        self.assertIsNotNone(playlist.token)


class VideoTestCase(TestCase):
    """Tests for Videos"""

    def setUp(self):
        p = PlayList.objects.create(title="Test playlist")
        Video.objects.create(token="QH2-TGUlwu4", playlist=p)

    def test_title_is_fetched(self):
        """The title of the video should be retrieved from YouTube when saved."""
        v = Video.objects.get(token="QH2-TGUlwu4")
        self.assertEqual("Nyan Cat [original]", v.title)
