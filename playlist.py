"""Tools for managing the playlist of the bot."""

import random


class MusicQueue:

    def __init__(self):
        self.queue:list = list()
        self.current = None
        self.recently_played:list = list()

        self.shuffle:bool = False
        self.repeat:bool = False
        self.loop:bool = False

    def add(self, url: str, index: int = 0):
        """Add a song to the playlist's queue.
        
        Args:
            url (str): URL of the song to add to the Playlist.
            index (int, optional): Index to add the Song URL at. Defaults to 0.
        """
        
        self.queue.insert(index,url)

    def pop(self, index:int):        
        song_url:str = self.queue.pop(index)
        if self.loop:
            self.queue.append(song_url)
        if self.current != None:
            self.recently_played.append(self.current)    
        self.current = song_url
        return song_url

    def next(self) -> str:
        """
        throws: ExhaustedException if there is no next element.
        """
        
        if self.repeat:
            return self.current
        
        if (len(self.queue)) <= 0:
            raise ExhaustedException
        
        if self.shuffle:
            song_index = random.randrange(0, len(self.queue))
            return self.pop(song_index)
        
        return self.pop(0)

    def prev(self) -> str:
        """
        throws: ExhaustedException if there is no prev element.
        """
        if len(self.recently_played) <= 0:
            raise ExhaustedException
        
        return self.recently_played.pop(0)

    def default_mode(self):
        self.shuffle = False
        self.loop = False
        self.repeat = False

    def shuffle_mode(self):
        self.shuffle = not self.shuffle

    def loop_mode(self):
        self.loop = not self.loop

    def repeat_mode(self):
        self.repeat = not self.repeat

    def clear(self):
        self.queue.clear()
        self.current = None
        self.recently_played.clear()


class ExhaustedException(Exception):
    pass


if __name__ == '__main__':
    # Manually confirming that #shuffle() works.
    p = MusicQueue()
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
