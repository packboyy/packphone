import pygame
from settings import *
from tinytag import TinyTag

class musicplayer:
    nowplaying = None
    songplaying = False
    song_length = 0
    @classmethod
    def init(cls):
        pygame.init()
        pygame.mixer.init()
    @classmethod
    def play_music(cls, song):
        cls.nowplaying = song
        cls.songplaying = True
        pygame.mixer.music.load(song.path)
        cls.song_length = cls.get_audio_length(song.path)
        pygame.mixer.music.play()
    @classmethod
    def stop_music(cls):
        cls.songplaying = False
        pygame.mixer.music.stop()
    @classmethod
    def pause_music(cls):
        cls.songplaying = False
        pygame.mixer.music.pause()
    @classmethod
    def resume_music(cls):
        cls.songplaying = True
        pygame.mixer.music.unpause()
    @classmethod
    def set_volume(cls, volume):
        pygame.mixer.music.set_volume(volume)
    @classmethod
    def get_volume(cls):
        return pygame.mixer.music.get_volume()
    @classmethod
    def is_playing(cls):
        return pygame.mixer.music.get_busy()
    @classmethod
    def get_position_percentage(cls):
        current_pos = pygame.mixer.music.get_pos()
        if cls.song_length > 0 and current_pos > 0:
            return current_pos / cls.song_length
        else:
            return 0
    @classmethod
    def get_audio_length(cls, audio_file):
        audio = TinyTag.get(audio_file)
        return int(audio.duration * 1000)
    @classmethod
    def quit(cls):
        pygame.mixer.quit()
        pygame.quit()