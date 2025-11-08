import pygame
from config import *
from object import *


class ScrollBarPointer(Object):
    def __init__(self, left, top, width, height, scroll_size, type):
        super().__init__(left, top, width, height)
        self.scroll_size = scroll_size
        self.type = type

    def change_pos(self, distance_per):
        if self.type == SCROLL_BAR_X:
            tmp_size = self.width
        else:
            tmp_size = self.height
        tmp_pos = (self.scroll_size-tmp_size) * distance_per
        if tmp_pos < 0:
            tmp_pos = 0
        elif tmp_pos  > self.scroll_size-tmp_size:
            tmp_pos = self.scroll_size-tmp_size
        if self.type == SCROLL_BAR_X:
            self.left = tmp_pos
        else:
            self.top = tmp_pos

    def show(self, surface):
        self.surface.fill(DARK_GRAY)
        super().show(surface)


class ScrollBar(Button):
    def __init__(self, left, top, width, height, sub_obj_size, show_obj_size, type, scroll):
        super().__init__(left, top, width, height, sub_objects=[])
        self.type = type
        if type == SCROLL_BAR_X:
            self.pointer = ScrollBarPointer(0, 0, show_obj_size/sub_obj_size*self.width, self.height, self.width, type)
        else :
            self.pointer = ScrollBarPointer(0, 0, self.width, show_obj_size/sub_obj_size*self.height, self.height, type)
        
        self.tracking = 0
        self.sub_objects.append(self.pointer)
        self.mother = scroll
        self.clicking = False

    def change_pos(self, distance_per):
        self.pointer.change_pos(distance_per)

    def event(self, event):
        if not self.is_on_me(): return None
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.clicking = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.clicking = False
        if self.clicking:
            if self.type == SCROLL_BAR_X:
                self.tracking = pygame.mouse.get_pos()[0]
                relative_pos = self.tracking

                if relative_pos < self.pointer.w/2:
                    relative_pos = self.pointer.w/2
                if relative_pos > self.w-self.pointer.w/2:
                    relative_pos = self.w-self.pointer.w/2
                tmp_val = (relative_pos-self.pointer.w/2)/(self.w-self.pointer.w)
                self.mother.change_pos(tmp_val, SCROLL_BAR_X)

            else:
                self.tracking = pygame.mouse.get_pos()[1]
                relative_pos = self.tracking-self.top

                if relative_pos < self.pointer.h/2:
                    relative_pos = self.pointer.h/2
                if relative_pos > self.h-self.pointer.h/2:
                    relative_pos = self.h-self.pointer.h/2
                # print(relative_pos, self.h, self.pointer.h)
                tmp_val = (relative_pos-self.pointer.h/2)/(self.h-self.pointer.h)
                self.mother.change_pos(tmp_val, SCROLL_BAR_Y)

    def show(self, surface):
        self.surface.fill(GRAY)
        super().show(surface)


class Scroll(Object):
    def __init__(self, sub_obj: Object, top, left, width, height, start_pos=[0, 0], surface=None, sub_objects=[]):
        super().__init__(top, left, width, height, surface, sub_objects)
        self.sub_obj = sub_obj
        self.sub_objects.append(sub_obj)
        self.show_pos = start_pos
        self.click_pos = [0, 0]
        self.wheel_acc = [0, 0]
        self.end_show_pos = [-self.sub_obj.size[i]+self.size[i] for i in range(2)]
        SCROLL_BAR_INTERVAL = 3
        SCROLL_BAR_HEIGHT = 10
        # print(self.rect.bottom-SCROLL_BAR_INTERVAL-SCROLL_BAR_HEIGHT)
        self.scrollx = ScrollBar(
            left=self.left+SCROLL_BAR_INTERVAL,
            top=self.bottom-SCROLL_BAR_INTERVAL-SCROLL_BAR_HEIGHT,
            width=self.width-SCROLL_BAR_INTERVAL*2-SCROLL_BAR_HEIGHT,
            height=SCROLL_BAR_HEIGHT,
            sub_obj_size=self.sub_obj.width,
            show_obj_size=self.width,
            type=SCROLL_BAR_X,
            scroll=self
        )
        # print(SCROLL_BAR_RECTX, SCROLL_BAR_RECTY)
        self.scrolly = ScrollBar(
            left=self.right-SCROLL_BAR_INTERVAL-SCROLL_BAR_HEIGHT,
            top=self.top+SCROLL_BAR_INTERVAL,
            width=SCROLL_BAR_HEIGHT,
            height=self.height-SCROLL_BAR_INTERVAL*2-SCROLL_BAR_HEIGHT,
            sub_obj_size=self.sub_obj.height,
            show_obj_size=self.height,
            type=SCROLL_BAR_Y,
            scroll=self
        )

        self.sub_objects.append(self.scrollx)
        self.sub_objects.append(self.scrolly)

    def change_pos(self, distance_per, xy):
        if xy == SCROLL_BAR_X:
            self.show_pos[0] = -(self.sub_obj.w - self.w)*distance_per
        else:
            self.show_pos[1] = -(self.sub_obj.h - self.h)*distance_per

    def event(self, event):
        if event.type == pygame.MOUSEWHEEL:
            self.wheel_acc[0] -= event.x * SCROLL_SPEED_X
            self.wheel_acc[1] += event.y * SCROLL_SPEED_Y
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.click_on = pygame.mouse.get_pos()
            self.sub_obj.event(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.click_on == pygame.mouse.get_pos():
                self.sub_obj.event(event)
        super().event(event)

    def show(self, surface):
        self.surface.fill(WHITE)
        self.sub_obj.topleft = self.show_pos
        self.sub_obj.show(self.surface)
        self.scrollx.change_pos(-1*self.show_pos[0]/(self.sub_obj.width-self.width))
        self.scrolly.change_pos(-1*self.show_pos[1]/(self.sub_obj.height-self.height))

        pygame.draw.rect(self.surface, RED, pygame.rect.Rect(3, 757, 1184, 10), width=1, border_radius=1)
        super().show(surface)

        for i in range(2):
            if self.wheel_acc[i] <= 1 and self.wheel_acc[i] >= -1:
                self.wheel_acc[i] = 0
            else:
                self.wheel_acc[i] //= 5
            self.show_pos[i] += self.wheel_acc[i]
            if self.show_pos[i] > 0:
                self.show_pos[i] = 0
            if self.show_pos[i] < self.end_show_pos[i]:
                self.show_pos[i] = self.end_show_pos[i]
