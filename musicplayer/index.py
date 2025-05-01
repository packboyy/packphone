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
    def add_song_to_index(music_index, songpath):
        tags = TinyTag.get(songpath, image=False)
        artist = tags.artist or "Unknown"
        album = tags.album or "Unknown"
        title = tags.title or os.path.basename(songpath)
        tracknumber = tags.track
        
        if artist not in music_index["artists"]:
            music_index["artists"][artist] = {"albums": {}}
        
        if album not in music_index["artists"][artist]["albums"]:
            music_index["artists"][artist]["albums"][album] = {"songs": []}

        music_index["artists"][artist]["albums"][album]["songs"].append({
        "title": title,
        "path": songpath,
        "tracknumber": tracknumber
        })
    
        music_index["artists"][artist]["albums"][album]["songs"].sort(
        key=lambda x: int(x["tracknumber"]) if x["tracknumber"] and str(x["tracknumber"]).isdigit() else float('inf')
        )

    @staticmethod
    def load_or_build_index():
        if os.path.exists(index.INDEX_FILE):
            with open(index.INDEX_FILE, 'r') as f:
                index.music_index = json.load(f)
            # check for missing songs and remove them ---------------------------------
            for artist in list(index.music_index["artists"].keys()):
                for album in list(index.music_index["artists"][artist]["albums"].keys()):
                    songs_to_keep = []
                    for song_data in index.music_index["artists"][artist]["albums"][album]["songs"]:
                        #add songs that exist to a list ---------------------------------
                        if os.path.exists(song_data["path"]):
                            songs_to_keep.append(song_data)
                    # update songs list with only existing files ---------------------------------
                    index.music_index["artists"][artist]["albums"][album]["songs"] = songs_to_keep
                    
                    #remove empty albums ---------------------------------
                    if len(songs_to_keep) == 0:
                        del index.music_index["artists"][artist]["albums"][album]
                
                # remove artists with no albums ---------------------------------
                if len(index.music_index["artists"][artist]["albums"]) == 0:
                    del index.music_index["artists"][artist]
            
            # scan for new songs ---------------------------------
            for root, dirs, files in os.walk("music"):
                for file in files:
                    if file.endswith(".mp3"):
                        songpath = os.path.join(root, file)
                        # check if song already exists in index ---------------------------------
                        song_exists = False
                        for artist in index.music_index["artists"]:
                            for album in index.music_index["artists"][artist]["albums"]:
                                for song_data in index.music_index["artists"][artist]["albums"][album]["songs"]:
                                    if song_data["path"] == songpath:
                                        song_exists = True
                                        break
                        
                        # add new song if not found ---------------------------------
                        if not song_exists:
                            index.add_song_to_index(index.music_index, songpath)
        else:
            # create new index if it doesn't exist ---------------------------------
            index.music_index = {"artists": {}}
            for root, dirs, files in os.walk("music"):
                for file in files:
                    if file.endswith(".mp3"):
                        songpath = os.path.join(root, file)
                        index.add_song_to_index(index.music_index, songpath)
        
        # save updated index ---------------------------------
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