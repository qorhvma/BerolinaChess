import pygame
from config import *


class Object:
    def __init__(self, rect, surface=None, sub_objects=[]):
        self.rect = rect
        self.surface = surface
        self._sub_objects = []z
        self.asb_pos = [0, 0]
        for i in sub_objects:
            self.insert_sub_objects(i)

    def show(self, surface):
        for obj in self.sub_objects:
            obj.show(self.surface)
        surface.blit(self.surface, self.rect)
        if DEBUG: pygame.draw.rect(surface, RED, self.rect, 1)

    def event(self, event):
        for obj in self.sub_objects:
            obj.event(event)

    def insert_sub_objects(self, val: object):
        val.asb_pos = [self.rect.left+self.asb_pos[0],
                       self.rect.top+self.asb_pos[1]]
        print(self, val, val.asb_pos)
        self._sub_objects.append(val)

    @property
    def sub_objects(self):
        return self._sub_objects

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, val):
        if not isinstance(val, pygame.rect.Rect):
            raise Exception(f'Object의 rect 값은 pygame.rect.Rect 객체여야 합니다. 현재 값: {val}')
        self._rect = val

    @property
    def surface(self):
        return self._surface

    @surface.setter
    def surface(self, val):
        if val is not None:
            self._surface = val
        elif self.rect is not None:
            self._surface = pygame.Surface(self.rect.size)
        else:
            self._surface = None



class Button(Object):
    def is_on_me(self):
        mx, my = pygame.mouse.get_pos()

        if self.rect.x+self.asb_pos[0]<=mx<=self.rect.x+self.asb_pos[0]+self.rect.width and self.rect.y+self.asb_pos[1]<=my<=self.rect.y+self.asb_pos[1]+self.rect.height:
            return True
        return False
