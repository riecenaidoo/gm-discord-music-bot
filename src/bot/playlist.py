"""Tools for managing the playlist of the bot."""

import logging
import utils

from random import randrange


_log = logging.getLogger(__name__)
_log.addHandler(utils.HANDLER)
_log.setLevel(logging.INFO)


class Playlist:
    def __init__(self):
        """Creates a structure that can manage the storage and retrieval
        of song urls in a manner that supports the primary music playlist features
        of queuing, shuffling, looping, and repeating.
        """

        self.song_queue: list = list()
        self.current_song = None
        self.recently_played_stack: list = list()

        self.shuffle: bool = False
        self.repeat: bool = False
        self.loop: bool = False

    class ExhaustedException(Exception):
        """Thrown if there are no more songs in the list the Playlist
        is trying to retrieve from.
        """

        pass

    def add(self, url: str, index: int = 0):
        """Add a song url to the playlist's queue.

        Args:
            url (str): URL to add to the Playlist.
            index (int, optional): Index to add the URL at. Defaults to 0.
        """

        self.song_queue.insert(index, url)

    def _pop(self, index: int = 0) -> str:
        """Removes and returns an element from the Playlist.

        Sets `current_song` to the removed element.
        Pushes the removed element to `recently_played_stack`.

        Args:
            index (int, optional): Song Index to remove. Defaults to 0.

        Returns:
            str: Song url string.
        """

        song_url: str = self.song_queue.pop(index)
        if self.loop:
            self.song_queue.append(song_url)
        if self.current_song is not None:
            self.recently_played_stack.append(self.current_song)
        self.current_song = song_url
        return song_url

    def next(self) -> str:
        """Retrieves the next song in the Playlist.
        Behaviour is modified by Playlist's `shuffle` `loop` `repeat` flags.

        - `shuffle`: pop a random song from `song_queue`.
        - `loop`:  pop a song from `song_queue` and append it back to the queue.
        - `repeat`: always return `current_song`, ignore the `song_queue`. If no
        'current_song' pop one from `song_queue`.

        Raises:
            ExhaustedException: if there is no next song in `song_queue`.

        Returns:
            str: next song's url.
        """

        if self.repeat:
            if not self.current_song:
                self.current_song = self._pop()

            return self.current_song

        if (len(self.song_queue)) <= 0:
            raise self.ExhaustedException

        if self.shuffle:
            rand_song_index = randrange(0, len(self.song_queue))
            return self._pop(rand_song_index)

        return self._pop()

    def prev(self) -> str:
        """Retrieves the previous song from the Playlist.

        Raises:
            ExhaustedException: if there is no previous song in `recently_played_stack`.

        Returns:
            str: previous song's url.
        """

        if len(self.recently_played_stack) <= 0:
            raise self.ExhaustedException

        return self.recently_played_stack.pop(0)

    def no_looping_mode(self):
        """Toggles looping modes off. Songs will not repeat again."""

        self.loop = False
        self.repeat = False
        _log.info("Loop/Repeat Mode: OFF")

    def shuffle_mode(self):
        """Toggles shuffle mode. Shuffling pops songs in a random order."""

        self.shuffle = not self.shuffle
        _log.info(f"Shuffle Mode: {'ON' if self.shuffle else 'OFF'}")

    def loop_mode(self):
        """Toggles loop all mode. Looping will append songs to the queue after they are popped off.
        Will unset repeat mode if it was enabled.
        """

        self.loop = not self.loop

        if self.loop and self.repeat:
            self.repeat = False
            _log.debug("Turning off Repeat Mode before enabling Loop Mode.")

        _log.info(f"Loop Mode: {'ON' if self.loop else 'OFF'}")

    def repeat_mode(self):
        """Toggles repeat mode. Repeating returns the currently popped song repeatedly."""

        self.repeat = not self.repeat
        _log.info(f"Repeat Mode: {'ON' if self.repeat else 'OFF'}")

    def clear(self):
        """Removes all songs from the Playlist."""

        self.song_queue.clear()
        self.current_song = None
        self.recently_played_stack.clear()
        _log.info("Cleared playlist.")


if __name__ == "__main__":
    # Randomness is hard to automatically test.
    # Run this to manually confirm that shuffling works.
    p = Playlist()
    p.add("a")
    p.add("b")
    p.add("c")
    p.add("d")
    p.add("e")
    p.shuffle_mode()
    print(p.next())
    print(p.next())
    print(p.next())
    print(p.next())
    print(p.next())
