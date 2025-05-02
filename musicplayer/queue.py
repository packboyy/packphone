import pygame
from tweener import *
from settings import *
from index import *
from musicplayer import musicplayer as mp

class queue:
    viewingqueue = False
    is_animating = False
    selected = 0
    last_selected = selected
    nowplaying = []
    songqueue = []
    linestodraw = []
    animation_speed = 0.4


    queuewidth = screen_width - 90
    pos = screen_width
    targetpos = 0
    selection_tween = Tween(0.0, 1.0, 70, Easing.QUAD, EasingMode.OUT)
    
    @staticmethod
    def get_selection_animation():
        if queue.last_selected != queue.selected:
            queue.selection_tween.start()
            queue.last_selected = queue.selected
        queue.selection_tween.update()
        return queue.selection_tween.value

    @staticmethod
    def animate(reversed):
        if queue.is_animating:
            queue.targetpos = screen_width if reversed else screen_width - queue.queuewidth
            distance = queue.targetpos - queue.pos
            queue.pos += distance * queue.animation_speed
            if abs(distance) < 2:
                queue.pos = queue.targetpos
                queue.is_animating = False
    
    @staticmethod
    def reset_animation(reversed=False):
        queue.is_animating = True
        
    @staticmethod
    def toggle():
        queue.linestodraw = queue.songqueue
        queue.viewingqueue = not queue.viewingqueue
        queue.is_animating = True
        queue.reset_animation(not queue.viewingqueue)

    @staticmethod
    def draw():
        # draw background
        pygame.draw.rect(screen, border_color, pygame.Rect((queue.pos-2, 0), (queue.queuewidth+2, screen_height)))
        pygame.draw.rect(screen, background_color, pygame.Rect((queue.pos, 0), (queue.queuewidth, screen_height)))

        # now playing
        font.render_to(screen, (queue.pos + padding, padding), str("Now Playing"), border_color)

        nowplayingsong = mp.nowplaying.songtitle if hasattr(mp.nowplaying, 'songtitle') else str("...")
        font_small.render_to(screen, (queue.pos + padding, (font_size + font_size_small)), str(nowplayingsong), border_color)
        nowplayingartist = mp.nowplaying.artist if hasattr(mp.nowplaying, 'artist') else str("...")
        font_small.render_to(screen, (queue.pos + queue.queuewidth - padding - font_small.get_rect(str(nowplayingartist)).width, (font_size + font_size_small*2)), str(nowplayingartist), border_color)

        # separator
        pygame.draw.rect(screen, border_color, pygame.Rect((queue.pos, (padding + font_size)*3 - padding), (queue.queuewidth, padding)))

        # queue text
        font.render_to(screen, (queue.pos + padding, padding + font_size*4), str("Queue"), border_color)
        for line, item in enumerate(queue.linestodraw):
            entrytext = item.songtitle if hasattr(item, 'songtitle') else item
            color = border_color if line == queue.selected else accent_color
            x_pos = queue.pos + padding
            if line == queue.selected:
                animation_value = queue.get_selection_animation()
                x_pos = queue.pos + padding + (padding * animation_value)
            font.render_to(screen, (x_pos, padding*2 + (font_size * 2) + (line+3) * font_size), str(entrytext), color)
    
    @staticmethod
    def playqueue():
        if mp.nowplaying == None:
            if queue.songqueue:
                mp.nowplaying = queue.songqueue[0]
                mp.play_music(mp.nowplaying)
                queue.songqueue.pop(0)
    
    @staticmethod
    def addtoqueue(entry):
        if hasattr(entry, 'songtitle'):
             queue.songqueue.append(entry)
        elif entry in artistindex:
            return
        elif entry in albumindex or entry in currentartist_albumindex:
            for artist in index.music_index["artists"]:
                if entry in index.music_index["artists"][artist]["albums"]:
                    for song_data in index.music_index["artists"][artist]["albums"][entry]["songs"]:
                        queue.songqueue.append(song(song_data["path"]))