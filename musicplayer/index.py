import json
import os
from tinytag import TinyTag

class song():
    def __init__(self, songpath):
        self.path = songpath
        tags = TinyTag.get(songpath, image=True)
        self.songtitle = tags.title or os.path.basename(songpath)
        self.artist = tags.artist or "Unknown"
        self.album = tags.album or "Unknown"
        self.tracknumber = tags.track
        self.albumart = tags.images.any.data

class index():
    INDEX_FILE = "music_index.json"
    music_index = None
    
    @staticmethod
    def load_or_build_index():
        if index.music_index:
            return index.music_index
            
        if os.path.exists(index.INDEX_FILE):
            with open(index.INDEX_FILE, 'r') as f:
                index.music_index = json.load(f)
        else:
            index.music_index = {"artists": {}}
            for root, dirs, files in os.walk("music"):
                for file in files:
                    if file.endswith(".mp3"):
                        songpath = os.path.join(root, file)
                        tags = TinyTag.get(songpath, image=False)
                        artist = tags.artist or "Unknown"
                        album = tags.album or "Unknown"
                        title = tags.title or os.path.basename(file)
                        
                        if artist not in index.music_index["artists"]:
                            index.music_index["artists"][artist] = {"albums": {}}
                        
                        if album not in index.music_index["artists"][artist]["albums"]:
                            index.music_index["artists"][artist]["albums"][album] = {"songs": []}
                        
                        index.music_index["artists"][artist]["albums"][album]["songs"].append({
                            "title": title,
                            "path": songpath
                        })
            
            with open(index.INDEX_FILE, 'w') as f:
                json.dump(index.music_index, f)
                
        return index.music_index

artistindex = []
albumindex = []
songindex = []
currentartist_albumindex = []
currentalbum_songindex = []

def refreshsongindex():
    songindex.clear()
    music_index = index.load_or_build_index()
    for artist in music_index["artists"]:
        for album in music_index["artists"][artist]["albums"]:
            for song_data in music_index["artists"][artist]["albums"][album]["songs"]:
                songindex.append(song(song_data["path"]))

def refreshalbumindex():
    albumindex.clear()
    music_index = index.load_or_build_index()
    for artist in music_index["artists"]:
        for album in music_index["artists"][artist]["albums"]:
            albumindex.append(album)

def refreshartistindex():
    artistindex.clear()
    music_index = index.load_or_build_index()
    for artist in music_index["artists"]:
        artistindex.append(artist)

def getalbumsfromartist(artist):
    currentartist_albumindex.clear()
    music_index = index.load_or_build_index()
    if artist in music_index["artists"]:
        for album in music_index["artists"][artist]["albums"]:
            currentartist_albumindex.append(album)

def getsongsfromalbum(album):
    currentalbum_songindex.clear()
    music_index = index.load_or_build_index()
    for artist in music_index["artists"]:
        if album in music_index["artists"][artist]["albums"]:
            for song_data in music_index["artists"][artist]["albums"][album]["songs"]:
                currentalbum_songindex.append(song(song_data["path"]))