import unittest

from playlist import MusicQueue, ExhaustedException


class TestMusicQueue(unittest.TestCase):

    def test_normal_next(self):
        playlist = MusicQueue()
        playlist.add("a")
        playlist.add("b")
        playlist.add("c")

        self.assertEqual(playlist.next(), "a")
        self.assertEqual(playlist.next(), "b")
        self.assertEqual(playlist.next(), "c")
        try:
            playlist.next()
            self.fail("Should throw an error!")
        except ExhaustedException:
            pass

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

    def test_prev(self):
        playlist = MusicQueue()
        playlist.add("a")
        playlist.add("b")
        playlist.add("c")
        playlist.next()
        playlist.next()
        playlist.next()

        self.assertEqual(playlist.prev(), "a")
        self.assertEqual(playlist.prev(), "b")
        self.assertEqual(playlist.prev(), "c")
        try:
            playlist.prev()
            self.fail("Should throw an error!")
        except ExhaustedException:
            pass
