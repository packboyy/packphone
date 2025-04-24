from tinytag import TinyTag
#catalog index
songindex = []
artistindex = []
currentartist_albumindex = []
currentalbum_songindex = []

class song():
    def __init__(self, songpath):
        self.path = songpath
        tags = TinyTag.get(songpath, image=True)
        self.songtitle = tags.title
        self.artist = tags.artist
        self.album = tags.album
        self.tracknumber = tags.track
        self.albumart = tags.images.any.data

class index():
    def refreshsongindex():
        songindex.clear()
        artistindex.clear()
        import os
        for root, dirs, files in os.walk("music"):
            for file in files:
                if file.endswith(".mp3"):
                    songpath = os.path.join(root, file)
                    new_song_entry = song(songpath)
                    songindex.append(new_song_entry)
    def refreshartistindex():
        for i in songindex:
            if i.artist not in artistindex:
                artistindex.append(i.artist)
    def getalbumsfromartist(artist):
        for i in songindex:
            if i.artist == artist:
                if i.album not in currentartist_albumindex:
                    currentartist_albumindex.append(i.album)
    def getsongsfromalbum(album):
        for i in songindex:
            if i.album == album:
                currentalbum_songindex.append(i)

    
    
