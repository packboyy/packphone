import pygame
from tinytag import TinyTag
from os import listdir
import io

#pygame
pygame.init()
pygame.freetype.init()
screen_width = 240
screen_height = 320
screen = pygame.display.set_mode((screen_width, screen_height), vsync=1)
pygame.display.set_caption("PackPager")

#styling
font_size = 16
font = pygame.freetype.Font("oxanium.ttf", font_size)
background_color = (255, 255, 255)
accent_color = (100, 240, 240)
border_color = (100, 100, 255)
catalogpadding = 40
padding = 5
songindex = []

running = True
songplaying = False



#catalog index
def refreshsongindex():
    songindex.clear
    for i in listdir("music"):
        if i.endswith(".mp3"):
            songpath = ('music/' + i)
            songtags = TinyTag.get(songpath, image=True)
            songindex.append([songpath, songtags])
refreshsongindex()

def clamp(n, min, max): 
    if n < min: 
        return min
    elif n > max: 
        return max
    else: 
        return n 

nowplaying = songindex[0]

def playsong(song):
    current_song_playing = pygame.mixer.music.load(song[0])
    pygame.mixer.music.play(0, 0)

def drawcover(song, pos, size):
    #ALBUM ART
    #turns binary shlock into readable image data
    img_data = io.BytesIO(song[1].images.any.data)
    album_art = pygame.transform.scale(pygame.image.load(img_data), pos)  
    screen.blit(album_art, size)

class catalog():
    viewingcatalog = False
    #catalog animation
    pos = -screen_width  # start off-screen to the left
    animation_speed = 0.4
    is_animating = True
    previous_catalog_state = False
    target_position = 0

    #selection
    selectedsong = 0

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
        pygame.draw.rect(screen, border_color, pygame.Rect((catalog.pos, 0), (screen_width-catalogpadding, screen_height)))
        pygame.draw.rect(screen, background_color, pygame.Rect((catalog.pos, 0), (screen_width-catalogpadding-2, screen_height)))
        line = 0
        for i in songindex:
            if line == catalog.selectedsong:
                font.render_to(screen, (catalog.pos + padding * 2, padding + line * font_size), str(i[1].title), border_color)
            else:
                font.render_to(screen, (catalog.pos + padding, padding + line * font_size), str(i[1].title), accent_color)
            line += 1
    
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

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                catalog.toggle()
            if event.key == pygame.K_SPACE:
                if songplaying:
                    pygame.mixer.stop()
                    songplaying = False
                else:
                    playsong(nowplaying)
                    songplaying = True
            if catalog.viewingcatalog:
                if event.key == pygame.K_DOWN:
                    catalog.selectedsong += 1
                    print(catalog.selectedsong)
                if event.key == pygame.K_UP:
                    catalog.selectedsong -= 1
                    print(catalog.selectedsong)
                if event.key == pygame.K_p:
                    nowplaying = songindex[catalog.selectedsong]
                    playsong(nowplaying)
                    catalog.toggle()
    
    screen.fill((background_color))

    #NOW LISTENING SCREEN
    # Draw album art
    pygame.draw.rect(screen, border_color, pygame.Rect(padding, padding, screen_width-(padding*2), screen_width-(padding*2)))
    drawcover(nowplaying, (screen_width-(padding*2)-4, screen_width-(padding*2)-4), (padding + 2, padding + 2))
    #song name
    font.render_to(screen, (padding, screen_width), str(nowplaying[1].title), border_color)
    #artist name
    font.render_to(screen, (padding, screen_width + padding + font_size), str(nowplaying[1].artist), border_color)

    # draw catalog if it's either fully visible or mid aniamtion
    if catalog.viewingcatalog or catalog.is_animating:
        catalog.animate(not catalog.viewingcatalog)
        catalog.drawcatalog()

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()