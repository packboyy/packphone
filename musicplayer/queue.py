import pygame
from tweener import *
from settings import *
from catalog import *
from musicplayer import musicplayer as mp

class queue:
    viewingqueue = False
    is_animating = False
    selected = 0
    nowplaying = []
    songqueue = []
    linestodraw = []
    animation_speed = 0.4


    queuewidth = screen_width - 90
    pos = screen_width
    targetpos = 0
    
    @staticmethod
    def animate(reversed):
        if queue.is_animating:
            distance = queue.targetpos - queue.pos
            queue.pos += distance * queue.animation_speed
            if abs(distance) < 2:
                queue.pos = queue.targetpos
                queue.is_animating = False
    
    @staticmethod
    def reset_animation(reversed=False):
        queue.pos = screen_width if reversed else screen_width - queue.queuewidth
        queue.targetpos = screen_width if reversed else screen_width - queue.queuewidth
        queue.is_animating = True
        
    @staticmethod
    def toggle():
        queue.linestodraw = queue.songqueue
        queue.viewingqueue = not queue.viewingqueue
        queue.is_animating = True
        queue.reset_animation(not queue.viewingqueue)

    @staticmethod
    def draw():
        pygame.draw.rect(screen, border_color, pygame.Rect((queue.pos-2, 0), (queue.queuewidth+2, screen_height)))
        pygame.draw.rect(screen, background_color, pygame.Rect((queue.pos, 0), (queue.queuewidth, screen_height)))
        font.render_to(screen, (queue.pos + padding, padding), str("Queue"), border_color)
        font.render_to(screen, (queue.pos + padding, padding + (font_size*2)), str(mp.nowplaying), border_color)
        for line, item in enumerate(queue.linestodraw):
            entrytext = item.songtitle if hasattr(item, 'songtitle') else item
            color = border_color if line == queue.selected else accent_color
            x_pos = queue.pos + padding
            if line == queue.selected:
                animation_value = catalog.get_selection_animation()
                x_pos = queue.pos + padding + (padding * animation_value)
            font.render_to(screen, (x_pos, padding + (font_size * 2) + (line+1) * font_size), str(entrytext), color)
    
    @staticmethod
    def playqueue():
        if mp.nowplaying == None:
            if queue.songqueue:
                mp.nowplaying = queue.songqueue[0]
                mp.play_music(mp.nowplaying)
                queue.songqueue.pop(0)