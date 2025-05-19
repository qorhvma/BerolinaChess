from typing import Callable
from config import *
import pygame


def binary_search(front : int, back : int, target : int, func : Callable[[int], int]) -> int :
    while front < back:
        mid = (front + back) // 2
        midVal = func(mid)
        if midVal > target:
            back = mid
        elif midVal < target:
            front = mid + 1
        else:
            return mid
    return front


def calculate_korean_font_size(size):
    height_val = binary_search(
        0,
        300,
        size[1],
        lambda S : pygame.font.SysFont(FONT, size=S).render('가', 1, BLACK).get_height()
    )
    width_val = binary_search(
        0,
        1000,
        size[0],
        lambda S : pygame.font.SysFont(FONT, size=height_val).render('가' * S, 1, BLACK).get_width()
    )
    return (height_val, width_val - 1)    # (폰트 크기, 글자 횟수)


class Object:
    def __init__(self, rect=None, surface=None, sub_objects=[]):
        self.rect = rect
        self.surface = surface
        self.sub_objects = sub_objects

    def show(self, surface):
        for obj in self.sub_objects:
            obj.show(self.surface)
        surface.blit(self.surface, self.rect)
    
    def event(self, event):
        for obj in self.sub_objects:
            obj.event(event)

    @property
    def surface(self):
        return self._surface
    
    @surface.setter
    def surface(self, val):
        if val:
            self._surface = val
        if self.rect:
            pygame.Surface(self.rect.size)


class Button(Object):
    def is_on_me(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.surface.rect.collidepoint(mouse_pos):
            return True
        return False


class Tab(Button):
    def __init__(self, text, size, page):
        self.text = text
        self.font = pygame.font.SysFont(FONT, size=calculate_korean_font_size(size)[0])
        self.textObj = self.font.render(self.text, 1, BLACK)
        self.rect = self.textObj.get_rect()
        self.rect.size = size
        self.page = page


class TabManager:
    def __init__(self, rect, tab_size=None, tab_color=None):
        self.rect = rect
        self.next_tab_pos = list(rect.topleft)
        self.tabs = []
        self.chosen = 0
        self.tab_size = (rect.width // 5, rect.height // 10) if not tab_size else tab_size
        self.tab_color = GRAY if not tab_color else tab_color

    def create_tab(self, title, page=Object(pygame.rect.Rect(0, 0, 100, 100))):
        self.tabs.append(Tab(title, self.tab_size, page))
        self.tabs[-1].rect.topleft = self.next_tab_pos
        self.tabs[-1].page.rect.topleft = (0, 0 + self.tab_size[1])
        intervel = 2
        self.next_tab_pos[0] += self.tab_size[0] + intervel

    def show(self, surface):
        for i, tab in enumerate(self.tabs):
            if i == self.chosen:
                pygame.draw.rect(surface, GRAY, tab.rect)
                x, y = self.rect.topleft
                tab.page.show(surface)
            else:
                pygame.draw.rect(surface, DARK_GRAY, tab.rect)
            surface.blit(tab.textObj, tab.rect)

    def event(self, event):
        for i, tab in enumerate(self.tabs):
            if tab.is_on_me():
                self.chosen = i


class Scroll(Object):
    def __init__(self, sub_obj, start_pos=[0, 0], *args, **kargs):
        super().__init__(*args, **kargs)
        self.sub_obj = sub_obj
        self.show_pos = start_pos
        self.click_pos = [0, 0]
    
    def event(self, event):
        if event.type == pygame.MOUSEWHEEL:
            self.show_pos[0] += event.x
            self.show_pos[1] += event.y
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.click_on = pygame.mouse.get_pos()
            self.sub_obj.event(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.click_on == pygame.mouse.get_pos():
                self.sub_obj.event(event)
        
    def show(self, surface):
        self.sub_obj.rect.topleft= self.show_pos
        self.sub_obj.show(self.surface)
        super().show(surface)
