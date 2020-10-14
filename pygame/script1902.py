# _*_ coding: utf-8 _*_
# @Time     : 2019/9/26 3:39
# @Author   : Ole211
# @Site     :
# @File     : script1902.py
# @Software : PyCharm

import pygame
import sys
import time
import random
from pygame.locals import *


def game():
    score = 0
    now = time.time()
    limt = 30
    future = now + limt
    pygame.init()
    pygame.mixer.init()
    ScreenSize = w, h = 1000, 700
    blue = 0, 0, 255
    red = 255, 0, 0
    white = 255, 255, 255
    RazPiRed = 210, 40, 82
    GameScreen = pygame.display.set_mode(ScreenSize)
    GameFont = pygame.font.Font('./fonts/msyh.ttf', 60)

    # Set up Time Text ##############################
    GameLimtText = 'Time: ' + str(limt) + ' s'
    GameLimtTextGraphic = GameFont.render(GameLimtText, True, white)
    GameScreen.blit(GameLimtTextGraphic, (500, 40))

    # Set up Image ####################################
    GameImage = 'horse.png'
    # GameImageGraphic = pygame.image.load(GameImage).convert_alpha()
    GameImageGraphic = pygame.image.load(GameImage)
    GameImageGraphic = pygame.transform.scale(GameImageGraphic, (200, 200))
    GameImageLocation = GameImageGraphic.get_rect()
    ImageOffset =[5, 5]
    # Set up Game Sound
    # ClickSound = pygame.mixer.Sound('test.wma')

    while True:
        if now > future:
            pygame.time.delay(3000)
            sys.exit()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 添加碰撞点，强制鼠标点击图像来结束游戏
                point_pos = pygame.mouse.get_pos()
                if GameImageLocation.collidepoint(point_pos):
                    # ClickSound.play()
                    print(point_pos)
                    score += 1
                    pygame.time.delay(500)
                    print('key down')
            if event.type == pygame.QUIT:
                sys.exit()
        if GameImageLocation.left < 0 or GameImageLocation.right > w:
            ImageOffset[0] = -ImageOffset[0]
        if GameImageLocation.top < 0 or GameImageLocation.bottom > h:
            ImageOffset[1] = -ImageOffset[1]
        # Move Game image
        GameImageLocation = GameImageLocation.move(ImageOffset)
        # Draw screen image
        GameScreen.fill(RazPiRed)
        GameScreen.blit(GameImageGraphic, GameImageLocation)
        # Draw screen SCORE text
        GameText = 'SCORE: ' + str(score)
        GameTextGraphic = GameFont.render(GameText, True, white)
        GameScreen.blit(GameTextGraphic, (500, 100))
        # Draw screen Time text
        limt = '%.2f' % (future - now)
        GameLimtText = 'Time: ' + str(limt) + ' s'
        GameLimtTextGraphic = GameFont.render(GameLimtText, True, white)
        GameScreen.blit(GameLimtTextGraphic, (500, 50))
        now = time.time()

        # update game screen
        pygame.display.update()


game()
