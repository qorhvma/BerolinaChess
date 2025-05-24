import pygame

class Object:
    def __init__(self, rect, surface=None, sub_objects=[], parent_pos=[0, 0]):
        self.rect = rect
        self.surface = surface
        self.sub_objects = sub_objects
        self.abs_pos = parent_pos

    def show(self, surface):
        for obj in self.sub_objects:
            obj.show(self.surface)
        surface.blit(self.surface, self.rect)
    
    def event(self, event):
        for obj in self.sub_objects:
            obj.event(event)

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
    
    @property
    def sub_objects(self):
        return self._sub_objects
    
    @sub_objects.setter
    def sub_objects(self, val):
        self._sub_objects = val

class Button(Object):
    def is_on_me(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            return True
        return False