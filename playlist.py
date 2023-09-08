"""Tools for managing the playlist of the bot."""

import random


class MusicQueue:

    def __init__(self):
        self.song_queue:list = list()
        self.current_song = None
        self.recently_played_stack:list = list()

        self.shuffle:bool = False
        self.repeat:bool = False
        self.loop:bool = False

    def add(self, url: str, index: int = 0):
        """Add a song url to the playlist's queue.

        Args:
            url (str): URL to add to the Playlist.
            index (int, optional): Index to add the URL at. Defaults to 0.
        """
        
        self.song_queue.insert(index,url)

    def pop(self, index:int = 0) -> str:    
        """Removes and returns an element from the Playlist.
        
        Sets `current_song` to the removed element.
        Pushes the removed element to `recently_played_stack`.

        Args:
            index (int, optional): Song Index to remove. Defaults to 0.

        Returns:
            str: Song url string.
        """ 
        
        song_url:str = self.song_queue.pop(index)
        if self.loop:
            self.song_queue.append(song_url)
        if self.current_song != None:
            self.recently_played_stack.append(self.current_song)    
        self.current_song = song_url
        return song_url

    def next(self) -> str:
        """
        throws: ExhaustedException if there is no next element.
        """
        
        if self.repeat:
            return self.current_song
        
        if (len(self.song_queue)) <= 0:
            raise ExhaustedException
        
        if self.shuffle:
            rand_song_index = random.randrange(0, len(self.song_queue))
            return self.pop(rand_song_index)
        
        return self.pop()

    def prev(self) -> str:
        """
        throws: ExhaustedException if there is no prev element.
        """
        
        if len(self.recently_played_stack) <= 0:
            raise ExhaustedException
        
        return self.recently_played_stack.pop(0)

    def default_mode(self):
        """Set playlist to default mode. Pops songs off in sequence.
        """
        
        self.shuffle = False
        self.loop = False
        self.repeat = False

    def shuffle_mode(self):
        """Toggles shuffle mode. Shuffling pops songs in a random order.
        """
        self.shuffle = not self.shuffle

    def loop_mode(self):
        """Toggles loop all mode. Looping will append songs to the queue after they are popped off.
        Will unset repeat mode if it was enabled.
        """
        
        self.loop = not self.loop
        
        if self.loop and self.repeat:
            self.repeat = False

    def repeat_mode(self):
        """Toggles repeat mode. Repeating returns the currently popped song repeatedly.
        """
        self.repeat = not self.repeat

    def clear(self):
        """Removes all songs from the Playlist.
        """
        self.song_queue.clear()
        self.current_song = None
        self.recently_played_stack.clear()


class ExhaustedException(Exception):
    """Thrown if there are no more songs in the list the Playlist 
    is trying to retrieve from.
    """
    pass


if __name__ == '__main__':
    # Randomness is hard to automatically test. 
    # Run this to manually confirm that shuffling works.
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
    print(p.next())