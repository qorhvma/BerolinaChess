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

    def show(self, surface: pygame.Surface):
        if self.is_on_me():
            self.surface.set_alpha(128)
        pygame.draw.rect(surface, self.normal_color, self)
        super().show(surface)
        self.surface.set_alpha(1000)


class PieceGenButtonGenButton(Button):
    def __init__(self, left, top, width, height, callbackfunc, surface=None, sub_objects=[]):
        super().__init__(left, top, width, height, surface, sub_objects)
        self.callbackfunc = callbackfunc
        self.font = pygame.font.SysFont(FONT, calculate_korean_font_size(self.size)[0])
        self.surface.blit(self.font.render("기물 생성", 1, WHITE), (0, 0, self.w, self.h))

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if (self.is_on_me()):
                self.callbackfunc()


class PieceGenScreen(Object):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.itval = 10
        self.button_size = (100, 100)
        self.button_pos = [10, 0]

    def create_button(self):
        file_path = filedialog.askopenfilename(
            title="파일을 선택하세요",
            filetypes=[("모든 파일", "*.png, *.jpg")]
        )
        try:
            image = pygame.image.load(file_path)
            image = pygame.transform.scale(image, self.button_size)
        except FileNotFoundError:
            print("파일 불러오기 실패")
            return
        self.sub_objects.insert(0, PieceGenButton(
            surface=image, 
            left=self.button_pos[0],
            top=self.button_pos[1],
            width=self.button_size[0],
            height=self.button_size[1]
        ))
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
        self.main_tab = TabManager(0, 0, WIDTH, HEIGHT, tab_size)
        self.piece_gen_screen = PieceGenScreen(
            0, 0, WIDTH * 3, (HEIGHT - tab_size[1]) * 3,
            pygame.transform.scale(pygame.image.load('dumpImage.png'), (WIDTH * 3, (HEIGHT - tab_size[1]) * 3))
        )
        self.scroll_piece_gen_screen = Scroll(
            self.piece_gen_screen,
            0, 0, WIDTH, HEIGHT - tab_size[1],
        )
        piecegenbuttongenbutton = PieceGenButtonGenButton(WIDTH-250, HEIGHT-100, 200, 50, self.piece_gen_screen.create_button)
        self.scroll_piece_gen_screen.sub_objects.append(piecegenbuttongenbutton)
        self.main_tab.create_tab('기물 생성', self.scroll_piece_gen_screen)
        self.main_tab.create_tab('지형 생성')
        self.main_tab.create_tab(
            '기물 배열',
            Object(0, 0, 100, 100, pygame.image.load('dumpImage.png'))
            )

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
            self.main_tab.event(event=event)
            self.scroll_piece_gen_screen.event(event=event)

    def end(self):
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    program = main()
    program.run()
