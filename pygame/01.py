# _*_ coding: utf-8 _*_
# @Time     : 2019/9/26 1:55
# @Author   : Ole211
# @Site     : 
# @File     : 01.py    
# @Software : PyCharm

import pygame
import sys

pygame.init()
size = w, h = 320, 240
screen = pygame.display.set_mode(size)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

pygame.quit()
