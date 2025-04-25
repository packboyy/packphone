import pygame
from settings import *
from musicplayer import *
from index import *
index.refreshsongindex()
index.refreshartistindex()
class catalog():
    page = 'Index'
    viewingcatalog = False
    #catalog animation
    pos = -screen_width  # start off-screen to the left
    animation_speed = 0.4
    is_animating = True
    previous_catalog_state = False
    target_position = 0
    #selection
    selected = 0

    linestodraw = []

    def animate(reversed):
        if catalog.is_animating:
            if not reversed:
                catalog.target_position = 0
            else:
                catalog.target_position = -screen_width
            distance = catalog.target_position - catalog.pos

            # clamp movement
            min_movement = 5 if abs(distance) > 5 else abs(distance)
            if distance > 0:
                catalog.pos += max(distance * catalog.animation_speed, min_movement)
            else:
                catalog.pos += min(distance * catalog.animation_speed, -min_movement)
                
            #stop animating when closer than 2px
            if abs(distance) < 2:
                catalog.pos = catalog.target_position
                catalog.is_animating = False
    
    def reset_animation(reversed=False):
        if not reversed:
            catalog.pos = -screen_width
        else:
            catalog.pos = 0
        catalog.is_animating = True
    
    def drawcatalog():
        pygame.draw.rect(screen, border_color, pygame.Rect((catalog.pos, 0), (screen_width-catalogpadding+2, screen_height)))
        pygame.draw.rect(screen, background_color, pygame.Rect((catalog.pos, 0), (screen_width-catalogpadding, screen_height)))
        line = 0
        for i in catalog.linestodraw:
            entrytext = i
            if i in songindex:
                entrytext = i.songtitle
            if line == catalog.selected:
                font.render_to(screen, (catalog.pos + padding * 2, padding + (font_size * 2) + line * font_size), str(entrytext), border_color)
            else:
                font.render_to(screen, (catalog.pos + padding, padding + (font_size * 2) + line * font_size), str(entrytext), accent_color)
            line += 1
        #render header with pages
        headerwidth = (screen_width - catalogpadding - padding*2)
        pygame.draw.rect(screen, accent_color, pygame.Rect(catalog.pos + padding, (font_size * 2) - padding*2, screen_width - catalogpadding - padding*2, padding))
        if catalog.page == 'Index':
            font.render_to(screen, (catalog.pos + padding, padding), str(catalog.page), border_color)
            pygame.draw.rect(screen, border_color, pygame.Rect(catalog.pos + padding, (font_size * 2) - padding*2, headerwidth/3, padding))
        if catalog.page == 'Albums':
            font.render_to(screen, (catalog.pos + (screen_width-catalogpadding)/2 - font.get_rect(str(catalog.page)).width/2, padding), str(catalog.page), border_color)
            pygame.draw.rect(screen, border_color, pygame.Rect(catalog.pos + padding, (font_size * 2) - padding*2, headerwidth/3, padding))


        
    
    def toggle():
        catalog.viewingcatalog = (not catalog.viewingcatalog)
        catalog.is_animating = True
        if catalog.viewingcatalog:
            # opening the menu
            catalog.reset_animation(False)  # start from off-screen
        else:
            # closing the menu
            catalog.reset_animation(True)  # start from 0
            catalog.previous_catalog_state = catalog.viewingcatalog
    
    def select():
        if catalog.linestodraw[catalog.selected] in artistindex:
            index.getalbumsfromartist(catalog.linestodraw[catalog.selected])
            catalog.linestodraw = currentartist_albumindex
            catalog.selected = 0
        elif catalog.linestodraw[catalog.selected] in currentartist_albumindex:
            index.getsongsfromalbum(catalog.linestodraw[catalog.selected])
            catalog.linestodraw = currentalbum_songindex
            catalog.selected = 0
        elif catalog.linestodraw[catalog.selected] in songindex:
            nowplaying = catalog.linestodraw[catalog.selected]
            musicplayer.play_music(nowplaying)
            catalog.toggle()
            catalog.selected = 0
    def back():
        if catalog.linestodraw[catalog.selected] in artistindex:
            catalog.selected = 0
            catalog.toggle()
        elif catalog.linestodraw[catalog.selected] in currentartist_albumindex:
            index.getsongsfromalbum(catalog.linestodraw[catalog.selected])
            catalog.linestodraw = artistindex
            catalog.selected = 0
            currentartist_albumindex.clear()
        elif catalog.linestodraw[catalog.selected] in songindex:            
            index.getalbumsfromartist(catalog.linestodraw[catalog.selected])
            catalog.linestodraw = currentartist_albumindex
            catalog.selected = 0
            currentalbum_songindex.clear()
        currentalbum_songindex.clear()