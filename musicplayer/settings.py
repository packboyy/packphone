import pygame
import pygame.freetype

#pygame
pygame.init()
pygame.freetype.init()
screen_width = 240
screen_height = 320
screen = pygame.display.set_mode((screen_width, screen_height), vsync=1)
pygame.display.set_caption("PackPager")

#styling
font_size = 16
font = pygame.freetype.Font('oxanium.ttf', font_size)
background_color = (255, 255, 255)
accent_color = (100, 190, 240)
border_color = (100, 100, 255)
catalogpadding = 40
padding = 5

def clamp(n, min, max): 
    if n < min:
        return min
    elif n > max:
        return max
    else: 
        return n