import pygame
from settings import *
from catalog import *
from queue import *
from musicplayer import musicplayer as mp

running = True
songplaying = False

#   assets
pause_icon = pygame.image.load('ui/pause.png')
play_icon = pygame.image.load('ui/play.png')
back_icon = pygame.image.load('ui/back.png')
forward_icon = pygame.image.load('ui/forward.png')
catalog.linestodraw = artistindex

playingicon = tintedsprite()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                if queue.viewingqueue == False:
                    catalog.toggle()
            if event.key == pygame.K_r:
                if catalog.viewingcatalog == False:
                    queue.toggle()
            if event.key == pygame.K_SPACE:
                if mp.songplaying:
                    mp.pause_music()
                else:
                    mp.resume_music()
            if catalog.viewingcatalog:
                if event.key == pygame.K_s:
                    catalog.selected += 1
                    catalog.selected = clamp(catalog.selected, 0, len(catalog.linestodraw) - 1)
                if event.key == pygame.K_w:
                    catalog.selected -= 1
                    catalog.selected = clamp(catalog.selected, 0, len(catalog.linestodraw) - 1)
                if event.key == pygame.K_d:
                    catalog.select()
                if event.key == pygame.K_a:
                    catalog.back()
                if event.key == pygame.K_e:
                    catalog.scroll(True)
                if event.key == pygame.K_q:
                    catalog.scroll(False)
                if event.key == pygame.K_r:
                    queue.addtoqueue(catalog.linestodraw[catalog.selected])
            elif queue.viewingqueue:
                if event.key == pygame.K_s:
                    queue.selected += 1
                    queue.selected = clamp(queue.selected, 0, len(queue.linestodraw) - 1)
                if event.key == pygame.K_w:
                    queue.selected -= 1
                    queue.selected = clamp(queue.selected, 0, len(queue.linestodraw) - 1)
    
    screen.fill((background_color))
    queue.playqueue()
    # NOW LISTENING SCREEN
    pygame.draw.rect(screen, border_color, pygame.Rect(padding, padding, screen_width-(padding*2), screen_width-(padding*2)))
    if mp.nowplaying:
        if not hasattr(mp, 'current_cover') or mp.nowplaying != mp.last_played:
            mp.current_cover = cover(mp.nowplaying)
            mp.last_played = mp.nowplaying
        mp.current_cover.draw((screen_width-(padding*2)-4, screen_width-(padding*2)-4), (padding + 2, padding + 2))

    # song and artist name
    song_title = mp.nowplaying.songtitle if mp.nowplaying and hasattr(mp.nowplaying, 'songtitle') else '...'
    font.render_to(screen, (padding, screen_width), str(song_title), border_color)
    artist_name = mp.nowplaying.artist if mp.nowplaying else '...'
    font.render_to(screen, (padding, screen_width + padding + font_size), str(artist_name), border_color)
    album_name = mp.nowplaying.album if mp.nowplaying else '...'
    font.render_to(screen, (screen_width-padding - font.get_rect(album_name).width, screen_width + padding + font_size), str(album_name), border_color)
    
    # SONG POSITION BAR
    pygame.draw.rect(screen, accent_color, pygame.Rect(padding, screen_width + (2*padding) + (2*font_size), (screen_width-(padding*2)), 10))
    pygame.draw.rect(screen, border_color, pygame.Rect(padding, screen_width + (2*padding) + (2*font_size), ((screen_width-padding) * mp.get_position_percentage()), 10))
    
    # PLAY/PAUSE ICON
    if mp.is_playing():
        playingicon.draw(pause_icon, border_color, (padding, screen_width + (2*padding) + (3*font_size)))
    else:
        playingicon.draw(play_icon, border_color, (padding, screen_width + (2*padding) + (3*font_size)))
    
    # draw catalog if it's either fully visible or mid animation
    if catalog.viewingcatalog or catalog.is_animating:
        catalog.animate(not catalog.viewingcatalog)
        catalog.drawcatalog()
    if queue.viewingqueue or queue.is_animating:
        queue.animate(not queue.viewingqueue)
        queue.draw()
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()