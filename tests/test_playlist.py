import unittest

from playlist import MusicQueue


class TestMusicQueue(unittest.TestCase):

    def test_normal_next(self):
        playlist = MusicQueue()
        playlist.add("a")
        playlist.add("b")
        playlist.add("c")

        self.assertEqual(playlist.next(), "a")
        self.assertEqual(playlist.next(), "b")
        self.assertEqual(playlist.next(), "c")
        self.assertEqual(playlist.next(), None)

    def test_loop_next(self):
        playlist = MusicQueue()
        playlist.add("a")
        playlist.add("b")
        playlist.add("c")
        playlist.loop()

        self.assertEqual(playlist.next(), "a")
        self.assertEqual(playlist.next(), "b")
        self.assertEqual(playlist.next(), "c")
        self.assertEqual(playlist.next(), "a")
        self.assertEqual(playlist.next(), "b")
        self.assertEqual(playlist.next(), "c")

    def test_repeat_next(self):
        playlist = MusicQueue()
        playlist.add("a")
        playlist.add("b")
        playlist.add("c")
        playlist.repeat()

        self.assertEqual(playlist.next(), "a")
        self.assertEqual(playlist.next(), "a")
        self.assertEqual(playlist.next(), "a")
