"""Tools for managing the playlist of the bot."""

import random
from enum import Enum


class PlaylistMode(Enum):
    SEQUENCE = 0
    SHUFFLE = 1
    LOOP = 2
    REPEAT = 3


class MusicQueue:

    def __init__(self):
        self.playlist = list()
        self.recently_played = list()
        self.mode = PlaylistMode(PlaylistMode.SEQUENCE)

    def add(self, url: str):
        self.playlist.append(url)

    def next(self) -> str:
        if self.mode == PlaylistMode.SEQUENCE:
            if len(self.playlist) <= 0:
                raise ExhaustedException
            song = self.playlist.pop(0)
            self.recently_played.append(song)
            return song
        elif self.mode == PlaylistMode.SHUFFLE:
            if len(self.playlist) <= 0:
                raise ExhaustedException
            i = random.randint(0, len(self.playlist))
            song = self.playlist.pop(i)
            self.recently_played.append(song)
            return song
        elif self.mode == PlaylistMode.REPEAT:
            return self.playlist[0]
        elif self.mode == PlaylistMode.LOOP:
            pass

    def prev(self) -> str:
        return self.recently_played.pop(len(self.recently_played) - 1)

    def normal(self):
        self.mode = PlaylistMode(PlaylistMode.SEQUENCE)

    def shuffle(self):
        self.mode = PlaylistMode(PlaylistMode.SHUFFLE)

    def loop(self):
        self.mode = PlaylistMode(PlaylistMode.LOOP)

    def repeat(self):
        self.mode = PlaylistMode(PlaylistMode.REPEAT)

    def clear(self):
        self.playlist = list()


class ExhaustedException(Exception):
    pass
