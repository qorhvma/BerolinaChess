from typing import Callable
import pygame

pygame.init()
BLACK = (0, 0, 0)


'''
<제작 코드>
작성 할 공간 (x, y) 값이 주어지면,
그 공간에 최적화 된 폰트 크기 반환 함수
'''


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
        lambda S : pygame.font.SysFont('nanumgothic', size=S).render('가', 1, BLACK).get_height()
    )
    width_val = binary_search(
        0,
        1000,
        size[0],
        lambda S : pygame.font.SysFont('nanumgothic', size=height_val).render('가' * S, 1, BLACK).get_width()
    )
    return (height_val, width_val - 1)


# for S in range(1, 100):
#     KoreanFont = pygame.font.SysFont('nanumgothic', size=S)
#     print(f'size:{S} -> Rect:{KoreanFont.render('한', 0, BLACK).get_rect()}')
