import pygame
from tweener import *
from settings import *
from musicplayer import *
from index import *

refreshsongindex()
refreshalbumindex()
refreshartistindex()
playlistindex = []

class catalog():
    page = 'Artists'
    viewingcatalog = False
    selected = 0
    catalogpage = 0
    headerwidth = (catalogwidth - padding*2)
    catalogpagepadding = 0
    
    pos = -catalogwidth
    animation_speed = 0.4
    is_animating = True
    target_position = 0
    
    linestodraw = []
    artistsPagesIndex = []
    albumsPagesIndex = []
    playlistsPagesIndex = []
    currentPagesIndex = artistsPagesIndex
    
    PAGE_MAPS = {
        0: ('Artists', artistsPagesIndex, lambda: artistindex.copy()),
        1: ('Albums', albumsPagesIndex, lambda: albumindex.copy()),
        2: ('Playlists', playlistsPagesIndex, lambda: playlistindex.copy())
    }

    @staticmethod
    def get_selection_animation():
        if not hasattr(catalog, '_selection_tween') or catalog._last_selected != catalog.selected:
            catalog._selection_tween = Tween(0.0, 1.0, 70, Easing.QUAD, EasingMode.OUT)
            catalog._selection_tween.start()
            catalog._last_selected = catalog.selected
        
        catalog._selection_tween.update()
        return catalog._selection_tween.value

    @staticmethod
    def animate(reversed):
        if catalog.is_animating:
            catalog.target_position = -catalogwidth if reversed else 0
            catalog._catalog_tween = Tween(catalog.pos, catalog.target_position, 150, Easing.QUAD, EasingMode.OUT)
            distance = catalog.target_position - catalog.pos
            catalog.pos += distance * catalog.animation_speed
            if abs(distance) < 2:
                catalog.pos = catalog.target_position
                catalog.is_animating = False
    
    @staticmethod
    def reset_animation(reversed=False):
        catalog.pos = 0 if reversed else -catalogwidth
        catalog.is_animating = True
    
    @staticmethod
    def drawcatalog():
        pygame.draw.rect(screen, border_color, pygame.Rect((catalog.pos, 0), (screen_width-catalogpadding+2, screen_height)))
        pygame.draw.rect(screen, background_color, pygame.Rect((catalog.pos, 0), (screen_width-catalogpadding, screen_height)))
        
        for line, item in enumerate(catalog.linestodraw):
            entrytext = item.songtitle if hasattr(item, 'songtitle') else item
            color = border_color if line == catalog.selected else accent_color
            x_pos = catalog.pos + padding
            if line == catalog.selected:
                animation_value = catalog.get_selection_animation()
                x_pos = catalog.pos + padding + (padding * animation_value)
            font.render_to(screen, (x_pos, padding + (font_size * 2) + line * font_size), str(entrytext), color)
            
        pygame.draw.rect(screen, accent_color, pygame.Rect(catalog.pos + padding, (font_size * 2) - padding*2, 
                                                         screen_width - catalogpadding - padding*2, padding))
                                                         
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
            musicplayer.play_music(selected_item)
            catalog.toggle()
            catalog.selected = 0
        elif selected_item in artistindex:
            current_stack.append([catalog.linestodraw, catalog.selected])
            getalbumsfromartist(selected_item)
            if currentartist_albumindex:
                catalog.linestodraw = currentartist_albumindex
                catalog.selected = 0
        elif selected_item in albumindex or selected_item in currentartist_albumindex:
            current_stack.append([catalog.linestodraw, catalog.selected])
            getsongsfromalbum(selected_item)
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
        if notreversed and catalog.catalogpage < 2:
            catalog.catalogpage += 1
            catalog.catalogpagepadding += catalog.headerwidth/3
        elif not notreversed and catalog.catalogpage > 0:
            catalog.catalogpage -= 1
            catalog.catalogpagepadding -= catalog.headerwidth/3
            
        if old_page != catalog.catalogpage:
            page_name, page_index, get_items = catalog.PAGE_MAPS[catalog.catalogpage]
            catalog.page = page_name
            catalog.currentPagesIndex = page_index
            catalog.linestodraw = get_items()
            catalog.selected = 0