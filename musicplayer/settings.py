import pygame
import pygame.freetype
import io
from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')

#pygame
pygame.init()
pygame.freetype.init()
screen_width = 240
screen_height = 320
screen = pygame.display.set_mode((screen_width, screen_height), vsync=1, flags=pygame.DOUBLEBUF)
pygame.display.set_caption("PackPager")

clock = pygame.time.Clock()
move_per_second = 500

#styling
font_size = config.getint('styling', 'font_size')
font = pygame.freetype.Font('oxanium.ttf', font_size)
font_size_small = config.getint('styling', 'font_size_small')
font_small = pygame.freetype.Font('oxanium.ttf', font_size_small)

background_color = pygame.Color(config['styling']['background_color'])
accent_color = pygame.Color(config['styling']['accent_color'])
border_color = pygame.Color(config['styling']['border_color'])

catalogpadding = 40
catalogwidth = (screen_width - catalogpadding)
padding = 5
programIcon = pygame.image.load('icon.png')
pygame.display.set_icon(programIcon)

def clamp(n, min, max): 
    if n < min:
        return min
    elif n > max:
        return max
    else: 
        return n
    
class tintedsprite():
    def __init__(self):
        self.cache = {}
        
    def draw(self, image, color, pos):
        color_tuple = (color.r, color.g, color.b, color.a)
        cache_key = (id(image), color_tuple)
        if cache_key not in self.cache:
            self.tinted = pygame.Surface(image.get_size())
            self.tinted.set_colorkey((255, 255, 255))
            self.tinted.fill(color)
            self.tinted.blit(image, (0, 0))
            self.cache[cache_key] = self.tinted
        screen.blit(self.cache[cache_key], pos)

class cover():
    def __init__(self, fromsong):
        self.img_data = io.BytesIO(fromsong.albumart)
        self.album_surface = pygame.image.load(self.img_data)
        
    def draw(self, size, pos):
        img = pygame.transform.scale(self.album_surface, size)
        img.convert_alpha()
        screen.blit(img, pos)