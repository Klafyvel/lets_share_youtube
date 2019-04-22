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
        Video.objects.create(token="QH2-TGUlwu4", playlist=p)
        Video.objects.create(token="QH2-TGUlwu4", playlist=p)

    def test_title_is_fetched(self):
        """The title of the video should be retrieved from YouTube when saved."""
        v = Video.objects.get(pk=1)
        self.assertEqual("Nyan Cat [original]", v.title)

    def test_index_creation(self):
        """When created, a video should be given an index in ascending order"""
        p = PlayList.objects.get(title="Test playlist")
        self.assertTrue(all(v.index == i + 1 for i, v in enumerate(p.video_set.all())))

    def test_down_index(self):
        """The nearest available index lesser than the current index should be attributed."""
        p = PlayList.objects.get(title="Test playlist")
        v = p.video_set.order_by("index").last()
        v.down_index()
        self.assertEqual(v.index, 2)
        self.assertEqual(p.video_set.order_by("index").last().index, 3)

        v.delete()
        v = p.video_set.order_by("index").last()
        v.down_index()
        self.assertEqual(v.index, 1)
        self.assertEqual(p.video_set.order_by("index").last().index, 3)

    def test_down_index_first(self):
        """If a video is already the first one, its index should not be downgraded."""
        p = PlayList.objects.get(title="Test playlist")
        v = p.video_set.order_by("index").first()
        v.down_index()
        self.assertEqual(v.index, 1)

    def test_up_index(self):
        """The nearest available index greater than the current index should be attributed."""
        p = PlayList.objects.get(title="Test playlist")
        v = p.video_set.order_by("index").first()
        v.up_index()
        self.assertEqual(v.index, 2)
        self.assertEqual(p.video_set.order_by("index").first().index, 1)

        v.delete()
        v = p.video_set.order_by("index").first()
        v.up_index()
        self.assertEqual(v.index, 3)
        self.assertEqual(p.video_set.order_by("index").first().index, 1)

    def test_up_index_last(self):
        """If a video is already the last one, its index should not be upgraded."""
        p = PlayList.objects.get(title="Test playlist")
        v = p.video_set.order_by("index").last()
        v.up_index()
        self.assertEqual(v.index, 3)
