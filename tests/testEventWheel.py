import pygame

class WheelTestObject:
    def __init__(self, rect=None, surface=None, sub_objects=[]):
        self.rect = rect
        self.surface = surface
        self.sub_objects = sub_objects

    def show(self, surface):
        for obj in self.sub_objects:
            obj.show(self.surface)
        surface.blit(self.surface, self.rect)

    def event(self, event):
        if event.type == pygame.MOUSEWHEEL:
            print(event.x, event.y)
    
    @property
    def surface(self):
        return self._surface
    
    @surface.setter
    def surface(self, val):
        if val:
            self._surface = val
        if self.rect:
            pygame.Surface(self.rect.size)