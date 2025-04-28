import pygame
from settings import *
from musicplayer import *
from index import *

index.refreshsongindex()
index.refreshalbumindex()
index.refreshartistindex()
playlistindex = []

class catalog():
    # catalog state
    page = 'Artists'
    viewingcatalog = False
    selected = 0
    catalogpage = 0
    headerwidth = (screen_width - catalogpadding - padding*2)
    catalogpagepadding = 0
    
    # animation properties
    pos = -screen_width  # start off-screen to the left
    animation_speed = 0.4
    is_animating = True
    target_position = 0
    
    linestodraw = []
    artistsPagesIndex = []
    albumsPagesIndex = []
    playlistsPagesIndex = []
    currentPagesIndex = artistsPagesIndex
    
    # page mapping
    PAGE_MAPS = {
        0: ('Artists', artistsPagesIndex, lambda: artistindex.copy()),
        1: ('Albums', albumsPagesIndex, lambda: albumindex.copy()),
        2: ('Playlists', playlistsPagesIndex, lambda: playlistindex.copy())
    }

    @staticmethod
    def animate(reversed):
        if catalog.is_animating:
            catalog.target_position = -screen_width if reversed else 0
            distance = catalog.target_position - catalog.pos

            # Clamp movement
            min_movement = 5 if abs(distance) > 5 else abs(distance)
            movement = max(distance * catalog.animation_speed, min_movement) if distance > 0 else min(distance * catalog.animation_speed, -min_movement)
            catalog.pos += movement
                
            # Stop animating when closer than 2px
            if abs(distance) < 2:
                catalog.pos = catalog.target_position
                catalog.is_animating = False
    
    @staticmethod
    def reset_animation(reversed=False):
        catalog.pos = 0 if reversed else -screen_width
        catalog.is_animating = True
    
    @staticmethod
    def drawcatalog():
        # draw background
        pygame.draw.rect(screen, border_color, pygame.Rect((catalog.pos, 0), (screen_width-catalogpadding+2, screen_height)))
        pygame.draw.rect(screen, background_color, pygame.Rect((catalog.pos, 0), (screen_width-catalogpadding, screen_height)))
        # draw list items
        for line, item in enumerate(catalog.linestodraw):
            entrytext = item.songtitle if hasattr(item, 'songtitle') else item
            color = border_color if line == catalog.selected else accent_color
            x_pos = catalog.pos + padding * 2 if line == catalog.selected else catalog.pos + padding
            font.render_to(screen, (x_pos, padding + (font_size * 2) + line * font_size), str(entrytext), color)
        # draw header with pages
        pygame.draw.rect(screen, accent_color, pygame.Rect(catalog.pos + padding, (font_size * 2) - padding*2, 
                                                           screen_width - catalogpadding - padding*2, padding))
        # draw tab with padding
        if catalog.page == 'Artists':
            text_pos = (catalog.pos + padding, padding)
        elif catalog.page == 'Albums':
            text_pos = (catalog.pos + (screen_width-catalogpadding)/2 - font.get_rect(str(catalog.page)).width/2, padding)
        else:
            text_pos = (catalog.pos + (screen_width-catalogpadding) - font.get_rect(str(catalog.page)).width - padding, padding)
        
        font.render_to(screen, text_pos, str(catalog.page), border_color)
        pygame.draw.rect(screen, border_color, pygame.Rect(catalog.pos + padding + catalog.catalogpagepadding, 
                                                          (font_size * 2) - padding*2, catalog.headerwidth/3, padding))
    
    @staticmethod
    def toggle():
        catalog.viewingcatalog = not catalog.viewingcatalog
        catalog.is_animating = True
        catalog.reset_animation(not catalog.viewingcatalog)
    
    @staticmethod
    def select():
        current_stack = catalog.get_current_stack()
        selected_item = catalog.linestodraw[catalog.selected]

        if hasattr(selected_item, 'songtitle'):
            print(f"Playing song: {selected_item.songtitle}")
            musicplayer.play_music(selected_item)
            catalog.toggle()
            catalog.selected = 0
        elif selected_item in artistindex:
            current_stack.append([catalog.linestodraw, catalog.selected])
            index.getalbumsfromartist(selected_item)
            if currentartist_albumindex:
                catalog.linestodraw = currentartist_albumindex
                catalog.selected = 0
        elif selected_item in albumindex or selected_item in currentartist_albumindex:
            current_stack.append([catalog.linestodraw, catalog.selected])
            index.getsongsfromalbum(selected_item)
            if currentalbum_songindex:
                catalog.linestodraw = currentalbum_songindex
                catalog.selected = 0
    
    @staticmethod
    def get_current_stack():
        return {
            0: catalog.artistsPagesIndex,
            1: catalog.albumsPagesIndex,
            2: catalog.playlistsPagesIndex
        }.get(catalog.catalogpage, catalog.artistsPagesIndex)
    
    @staticmethod
    def back():
        current_stack = catalog.get_current_stack()
        if current_stack:
            previous_page = current_stack.pop()
            catalog.linestodraw = previous_page[0]
            catalog.selected = previous_page[1]
    
    @staticmethod
    def scroll(notreversed):
        old_page = catalog.catalogpage
        # move the tab bar
        if notreversed and catalog.catalogpage < 2:
            catalog.catalogpage += 1
            catalog.catalogpagepadding += catalog.headerwidth/3
        elif not notreversed and catalog.catalogpage > 0:
            catalog.catalogpage -= 1
            catalog.catalogpagepadding -= catalog.headerwidth/3
        # only update if it actually changed pages
        if old_page != catalog.catalogpage:
            page_name, page_index, get_items = catalog.PAGE_MAPS[catalog.catalogpage]
            catalog.page = page_name
            catalog.currentPagesIndex = page_index
            catalog.linestodraw = get_items()
            catalog.selected = 0