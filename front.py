from typing import Callable
import pygame
from config import *
from scroll import *

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
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            for i, tab in enumerate(self.tabs):
                if tab.is_on_me():
                    self.chosen = i
