from typing import Callable
from config import *
from front import *
import pygame
import sys


class main:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(PROGRAM_NAME)
        self.SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True

        #객체 초기화
        self.main_tab = TabManager(pygame.rect.Rect(0, 0, WIDTH, HEIGHT), tab_size=(100, 30))
        self.main_tab.createTab('기물 생성', Object((100, 100), pygame.image.load('dumpImage.png')))
        self.main_tab.createTab('지형 생성')
        self.main_tab.createTab('기물 배열', Object((100, 100), pygame.image.load('dumpImage.png')))

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
                self.main_tab.event(mouse_pos)

    def end(self):
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    program = main()
    program.run()
