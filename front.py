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
    def __setattr__(self, name: str, val: Any) -> Any:
        return_val = super().__setattr__(name, val)
        pos_targets = ["x", "y", "topleft", "topright", "bottom","bottomleft",
                       "bottomright", "center", "centerx", "centery", "left",
                       "midbottom", "midleft", "midright", "midtop", "right", "top"]
        if (name in pos_targets):
            self.page.topleft = (0, self.h)
        return return_val

    def __init__(self, left: int, top: int, width: int, height: int, text: str, page: Object):
        super().__init__(left, top, width, height)
        self.text = text
        self.font = pygame.font.SysFont(FONT, size=calculate_korean_font_size(self.size)[0])
        self.textObj = self.font.render(self.text, 1, BLACK)
        self._page = page
        self.page.topleft = (0, self.h)

        self.chosen_color = DARK_GRAY
        self.default_color = GRAY

        self.surface = pygame.surface.Surface(self.size)
        self.change_color(False)

    def change_color(self, chosen):
        if (chosen):
            pygame.draw.rect(self.surface, self.chosen_color, (0, 0, self.width, self.height))
        else:
            pygame.draw.rect(self.surface, self.default_color, (0, 0, self.width, self.height))
        self.surface.blit(self.textObj, (0, 0, self.width, self.height))

    @property
    def page(self):
        return self._page

    @page.setter
    def page(self, val):
        self._page = val
        self.page.topleft = (0, self.h)


class TabManager(Object):
    def __init__(self, left, top, width, height, tab_size=None, tab_color=None):
        super().__init__(left, top, width, height)
        self.next_tab_pos: list = list(self.topleft)
        self.tabs : list[Tab] = []
        self.chosen = 0
        self.tab_size = (self.width // 5, self.height // 10) if not tab_size else tab_size
        self.tab_color = GRAY if not tab_color else tab_color

    def create_tab(self, title, page=Object(0, 0, 100, 100)): 
        self.tabs.append(Tab(
            left=self.next_tab_pos[0],
            top=self.next_tab_pos[1],
            width=self.tab_size[0],
            height=self.tab_size[1],
            text=title,
            page=page
        ))
        # self.tabs[-1].page.topleft = (0, 0 + self.tab_size[1])
        intervel = 2
        self.next_tab_pos[0] += self.tab_size[0] + intervel

    def show(self, surface):
        for i, tab in enumerate(self.tabs):
            tab.change_color(i == self.chosen)
            tab.show(surface)
            if (i == self.chosen):
                tab.page.show(surface)
        self.show_sub_objects(surface)

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            for i, tab in enumerate(self.tabs):
                if tab.is_on_me():
                    self.chosen = i
        return super().event(event)
