import pygame
from catalog import *
from settings import *
from musicplayer import musicplayer as mp
import io

running = True
songplaying = False

#assets
pause_icon = pygame.image.load('ui/pause.png')
play_icon = pygame.image.load('ui/play.png')
back_icon = pygame.image.load('ui/back.png')
forward_icon = pygame.image.load('ui/forward.png')
catalog.linestodraw = artistindex
def clamp(n, min, max): 
    if n < min: 
        return min
    elif n > max: 
        return max
    else: 
        return n

class tintedsprite():
    def draw(self, image, color, pos):
        tinted = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        img_array = pygame.surfarray.array_alpha(image)
        tinted.fill((color[0], color[1], color[2], 255))
        tinted_array = pygame.surfarray.pixels_alpha(tinted)
        # Copy the alpha values from the original to preserve transparency
        tinted_array[:] = img_array
        del tinted_array
        # Draw the result to screen
        screen.blit(tinted, pos)

class cover():
    def __init__(self, fromsong):
            self.img_data = io.BytesIO(fromsong.albumart)
            self.album_surface = pygame.image.load(self.img_data)
    def draw(self, pos, size):
        #ALBUM ART
        #turns binary shlock into readable image data
            album_art = pygame.transform.scale(self.album_surface, pos)
            screen.blit(album_art, size)

playingicon = tintedsprite()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                catalog.toggle()
            if event.key == pygame.K_SPACE:
                if mp.songplaying:
                    mp.pause_music()
                else:
                    mp.resume_music()
            if catalog.viewingcatalog:
                if event.key == pygame.K_DOWN:
                    catalog.selected += 1
                    catalog.selected = clamp(catalog.selected, 0, len(catalog.linestodraw) - 1)
                    print(catalog.selected)
                if event.key == pygame.K_UP:
                    catalog.selected -= 1
                    catalog.selected = clamp(catalog.selected, 0, len(catalog.linestodraw) - 1)
                    print(catalog.selected)
                if event.key == pygame.K_p:
                    catalog.select()
                if event.key == pygame.K_o:
                    catalog.back()
    
    screen.fill((background_color))

    #NOW LISTENING SCREEN
    # Draw album art
    pygame.draw.rect(screen, border_color, pygame.Rect(padding, padding, screen_width-(padding*2), screen_width-(padding*2)))
    if mp.nowplaying:
        bigcover = cover(mp.nowplaying)
        bigcover.draw((screen_width-(padding*2)-4, screen_width-(padding*2)-4), (padding + 2, padding + 2))

    #song and artist name
    song_title = mp.nowplaying.songtitle if mp.nowplaying and hasattr(mp.nowplaying, 'songtitle') else '...'
    font.render_to(screen, (padding, screen_width), str(song_title), border_color)
    artist_name = mp.nowplaying.artist if mp.nowplaying else '...'
    font.render_to(screen, (padding, screen_width + padding + font_size), str(artist_name), border_color)
    album_name = mp.nowplaying.album if mp.nowplaying else '...'
    font.render_to(screen, (screen_width-padding, screen_width + padding + font_size), str(album_name), border_color)
    #SONG POSITION BAR

    pygame.draw.rect(screen, accent_color, pygame.Rect(padding, screen_width + (2*padding) + (2*font_size), (screen_width-(padding*2)), 10))
    pygame.draw.rect(screen, border_color, pygame.Rect(padding, screen_width + (2*padding) + (2*font_size), ((screen_width-padding) * mp.get_position_percentage()), 10))
    if mp.is_playing():
        playingicon.draw(pause_icon, border_color, (padding, screen_width + (2*padding) + (3*font_size)))
    if not mp.is_playing():
        playingicon.draw(play_icon, border_color, (padding, screen_width + (2*padding) + (3*font_size)))
    
    # draw catalog if it's either fully visible or mid aniamtion
    if catalog.viewingcatalog or catalog.is_animating:
        catalog.animate(not catalog.viewingcatalog)
        catalog.drawcatalog()

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()