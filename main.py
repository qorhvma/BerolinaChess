import sys
import tkinter as tk
from tkinter import filedialog
from typing import Callable
import pygame
from config import *
from front import *
# 5/26 으아ㅏㅏㅏㅏㅏ


class PieceGenButton(Button):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.normal_color = DARK_GRAY
        self.diff_color = GRAY
    
    def show(self, surface):
        if self.is_on_me():
            pygame.draw.rect(surface, self.diff_color, self.rect)
        else:
            pygame.draw.rect(surface, self.normal_color, self.rect)


class PieceGenScreen(Object):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.itval = 10
        self.button_size = (30, 30)
        self.button_pos = [10, 0]
        #self.piece_buttons = []
        
    def create_button(self):
        file_path = filedialog.askopenfilename(
                title="파일을 선택하세요",
                filetypes=[("모든 파일", "*.png, *.jpg")]
            )
        image = pygame.image.load(file_path)
        rect = pygame.rect.Rect(self.button_pos[0], self.button_pos[1], self.button_size[0], self.button_size[1])
        self.sub_objects.append(PieceGenButton(surface=image, rect=rect))
        self.button_pos[0] += self.itval + self.button_size[0]


class main:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(PROGRAM_NAME)
        self.SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        root = tk.Tk()
        root.withdraw()

        #객체 초기화
        tab_size = (100, 30)
        self.main_tab = TabManager(pygame.rect.Rect(0, 0, WIDTH, HEIGHT), tab_size)
        piece_gen_screen = Object(pygame.rect.Rect(0, 0, WIDTH, HEIGHT-tab_size[1]), pygame.transform.scale(pygame.image.load('dumpImage.png'), (WIDTH, HEIGHT-30)))
        self.main_tab.create_tab('기물 생성', piece_gen_screen)
        self.main_tab.create_tab('지형 생성')
        self.main_tab.create_tab('기물 배열', Object(pygame.rect.Rect(0, 0, 100, 100), pygame.image.load('dumpImage.png')))

    def run(self):
        while self.running:
            self.SCREEN.fill(WHITE)
            self.event()
            self.main_tab.show(self.SCREEN)
            pygame.display.update()
        self.end()
    
    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                self.main_tab.event(event)

    def end(self):
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    program = main()
    program.run()
