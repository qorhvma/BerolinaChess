from KoreanTextSize2Rect import *
from testEventWheel import *
import pygame
import sys

# 화면 크기
HEIGHT = 800
WIDTH = 1200
PROGRAM_NAME = '변형 체스 생성 툴'

#색깔
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (125, 125, 125)

pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(PROGRAM_NAME)

rect_size = (1000, 20)
x, y = calculate_korean_font_size(rect_size)
text = pygame.font.SysFont('nanumgothic', size=x).render('안'*y, 1, BLACK)

running = True

x = WheelTestObject()

from pygame.locals import *
print()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        x.event(event)

    SCREEN.fill(WHITE)
    pygame.draw.rect(SCREEN, GREEN, (0, 0, rect_size[0], rect_size[1]))
    SCREEN.blit(text, text.get_rect())
    pygame.display.update()
