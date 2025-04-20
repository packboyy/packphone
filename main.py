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

#catalog index
def refreshsongindex():
    songindex.clear
    for i in listdir("music"):
        if i.endswith(".mp3"):
            songpath = ('music/' + i)
            songtags = TinyTag.get(songpath, image=True)
            songindex.append([songpath, songtags])
refreshsongindex()

selectedsong = songindex[0]

def playsong(song):
    current_song_playing = pygame.mixer.music.load(song[0])
    pygame.mixer.music.play(0, 0)

def drawcover(song, pos, size):
    #ALBUM ART
    #turns binary shlock into readable image data
    img_data = io.BytesIO(song[1].images.any.data)
    album_art = pygame.transform.scale(pygame.image.load(img_data), pos)  
    screen.blit(album_art, size) # Resize to your dimensions
class catalog():
    #catalog animation
    pos = -screen_width  # Start off-screen to the left
    target_position = 0  # Final resting position
    animation_speed = 0.1  # Adjust this to control animation speed
    def animatecatalog():
        is_animating = True
        # Only update if still animating
        if is_animating:
            # Ease toward the target position
            distance = catalog.target_position - catalog.pos
            catalog.pos += distance * catalog.animation_speed
            # Stop animating when we're close enough
            if abs(distance) < 1:
                catalog.pos = catalog.target_position
                is_animating = False
    def drawcatalog():
        catalog.animatecatalog()
        pygame.draw.rect(screen, border_color, pygame.Rect((catalog.pos, 0), (screen_width-catalogpadding, screen_height)))
        pygame.draw.rect(screen, background_color, pygame.Rect((catalog.pos, 0), (screen_width-catalogpadding-2, screen_height)))
        line = 0
        for i in songindex:
            line = line + 1
            font.render_to(screen, (padding, padding + line * font_size), str(i[1].title), border_color)
viewingcatalog = False
running = True
songplaying = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                viewingcatalog = (not viewingcatalog)
            if event.key == pygame.K_SPACE:
                if songplaying:
                    pygame.mixer.stop()
                    songplaying = False
                else:
                    playsong(selectedsong)
                    songplaying = True
    screen.fill((background_color))

    #NOW LISTENING SCREEN
    # Draw album art
    pygame.draw.rect(screen, border_color, pygame.Rect(padding, padding, screen_width-(padding*2), screen_width-(padding*2)))
    drawcover(selectedsong, (screen_width-(padding*2)-4, screen_width-(padding*2)-4), (padding + 2, padding + 2))
    #song name
    font.render_to(screen, (padding, screen_width), str(selectedsong[1].title), border_color)
    #artist name
    font.render_to(screen, (padding, screen_width + padding + font_size), str(selectedsong[1].artist), border_color)


    if viewingcatalog:
        catalog.drawcatalog()

    pygame.display.flip()
    pygame.time.Clock().tick(60)
pygame.quit()