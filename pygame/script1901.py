# _*_ coding: utf-8 _*_
# @Time     : 2019/9/26 2:07
# @Author   : Ole211
# @Site     : 
# @File     : script1901.py    
# @Software : PyCharm
# script1901.py - Simple Game Screen & Text
#
###########################################
#
##### Import Modules & Variable #####
import pygame     # import game library
import time       # load game constants
from pygame.locals import *
pygame.init()
pygame.mixer.init()

ScreenSize = (1000, 800)
GameScreen = pygame.display.set_mode(ScreenSize)
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
green = 0, 255, 0
RazPiRed = 210, 40, 82
blue = 0, 0, 255
GameScreen.fill(RazPiRed)
DefaultFont = None
GameFont = pygame.font.Font('./fonts/msyh.ttf', 60)
GameText = 'Hello, 大家好'
GameTextGraphic = GameFont.render(GameText, True, white)
GameScreen.blit(GameTextGraphic, (100, 100))
# Set up the Game Image Graphics
GameImage = 'd://img/f1_out_no_bg.png'
GameImageGraphic = pygame.image.load(GameImage).convert_alpha()
GameScreen.blit(GameImageGraphic, (300, 0))
# pygame.draw.circle(GameScreen, (100, 40, 240), (500, 300), 100, 10)

# Set up Game Sound
# ClickSound = pygame.mixer.Sound("TalkAnymore.mp3")
# ClickSound.play()
# pygame.time.delay(300)

# Set up Graphic Image Movement Speed
ImageOffset = [10,  10]
# Move Image around
GameImageLocation = GameImageGraphic.get_rect()
GameImageLocation = GameImageLocation.move(ImageOffset)
GameScreen.fill(blue)
GameScreen.blit(GameImageGraphic, GameImageLocation)
pygame.display.update()
time.sleep(10)


