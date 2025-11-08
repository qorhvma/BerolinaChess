from typing import Any, Iterable, SupportsIndex
import pygame
from config import *


class Object(pygame.rect.Rect):
    class sub_objects_list(list):
        def __init__(self, asb_pos_specifier):
            self.asb_pos_specifier = asb_pos_specifier
        def append(self, object: Any) -> None:
            self.asb_pos_specifier(object)
            return super().append(object)
        def insert(self, index: SupportsIndex, object: Any) -> None:
            self.asb_pos_specifier(object)
            return super().insert(index, object)
        def extend(self, iterable: Iterable) -> None:
            for i in iterable:
                self.asb_pos_specifier(i)
            return super().extend(iterable)
        def __setitem__(self, index, value):
            self.asb_pos_specifier(value)
            return super().__setitem__(index, value)


    def __setattr__(self, name: str, val: Any) -> Any:
        return_val = super().__setattr__(name, val)
        pos_targets = ["x", "y", "topleft", "topright", "bottom","bottomleft",
                       "bottomright", "center", "centerx", "centery", "left",
                       "midbottom", "midleft", "midright", "midtop", "right", "top"]
        if (name in pos_targets):
            self._change_sub_objects_asb_pos()
        return return_val

    def __init__(self, left: int, top: int, width: int, height: int, surface: pygame.Surface|None=None, sub_objects:list=[]):
        super().__init__(left, top, width, height)
        if (surface == None): 
            self.surface = pygame.Surface((width, height))
        else:
            self.surface = surface
        
        self._sub_objects = self.sub_objects_list(self._insert_sub_objects)
        self.sub_objects = sub_objects
        self._asb_pos = [0, 0]

    def show(self, surface):
        for obj in self.sub_objects:
            obj.show(self.surface)
        surface.blit(self.surface, self)
        if DEBUG: pygame.draw.rect(surface, RED, self, 1)

    def event(self, event):
        for obj in self.sub_objects:
            obj.event(event)
    
    def _insert_sub_objects(self, object):
        object.asb_pos=[self.asb_pos[0]+self.left, self.asb_pos[1]+self.top]
    
    def _change_sub_objects_asb_pos(self):
        for sub in self.sub_objects:
            sub.asb_pos = [self.x+self.asb_pos[0], self.y+self.asb_pos[1]]
    
    @property
    def asb_pos(self):
        return tuple(self._asb_pos)
    
    @asb_pos.setter
    def asb_pos(self, val):
        self._asb_pos = val

    @property
    def sub_objects(self):
        return self._sub_objects

    @sub_objects.setter
    def sub_objects(self, val: list):
        self._sub_objects.clear()
        for i in val:
            self._sub_objects.append(i)


class Button(Object):
    def is_on_me(self):
        mx, my = pygame.mouse.get_pos()

        if self.x+self.asb_pos[0]<=mx<=self.x+self.asb_pos[0]+self.w and self.y+self.asb_pos[1]<=my<=self.y+self.asb_pos[1]+self.h:
            return True
        return False

if __name__ == "__main__":
    test = Object(0, 0, 10, 10)
    test.x = 10
    test.size = (10, 10)
