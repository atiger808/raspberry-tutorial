# _*_ coding: utf-8 _*_
# @Time     : 2019/9/26 5:09
# @Author   : Ole211
# @Site     : 
# @File     : script1903.py    
# @Software : PyCharm

import pygame
import random
import sys
from pygame.locals import *
#
pygame.init()
#
##### Set up Rasberry ###########
#
# Delete a Raspberry
def deleteRaspberry(RaspberryDict, RNumber):
    key1 = 'RasLoc' + str(RNumber)
    key2 = 'RasOff' + str(RNumber)
    #
    # Make a copy Current Dictionary
    NewRaspberry = dict(RaspberryDict)
    del NewRaspberry[key1]
    del NewRaspberry[key2]
    return NewRaspberry
#
# Set up the Game Screen ###########
#
ScreenSize = ScreenWidth, ScreenHeight = 1000, 700
GameScreen = pygame.display.set_mode(ScreenSize)
#
# Set up the Game Color ############
blue = 0, 255, 255
#
# Set up the Game Image Graphic #####
GameImage = 'horse.png'
GameImageGraphic = pygame.image.load(GameImage)
GameImageGraphic = pygame.transform.scale(GameImageGraphic, (200,200))

GameImageLocation = GameImageGraphic.get_rect()
ImageOffset = [5, 5]   # Startig Speed
#
# Build the Raspberry Dictionanry
#
RAmount = 50  # Numer of Raspberries on screen
Raspberry = {}
#
for RNumber in range(RAmount):
    Position_x = (ImageOffset[0] + RNumber) * random.randint(9, 29)
    Position_y = (ImageOffset[1] + RNumber) * random.randint(8, 18)
    Location = GameImageLocation.move(Position_x, Position_y)
    RasKey = 'RasLoc' + str(RNumber)
    Raspberry[RasKey] = Location
    RasKey = 'RasOff' + str(RNumber)
    Raspberry[RasKey] = ImageOffset
#
#  Set up Game Sound #######
#
# ClickSound = pygame.mixer.Sound('')
#
######### Play Game ######################
#
while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            for RNumber in range(RAmount):
                RasLoc = 'RasLoc' + str(RNumber)
                RasImageLocation = Raspberry[RasLoc]
                if RasImageLocation.collidepoint(pygame.mouse.get_pos()):
                    deleteRaspberry(Raspberry, RNumber)
                    RAmount = RAmount - 1
                    # ClickSoumd.play()
                    pygame.time.delay(50)
                    if RAmount == 0:
                        sys.exit()
    # Redraw the Screen Background
    GameScreen.fill(blue)
    #
    # Move the Raspberries around the screen
    for RNumber in range(RAmount):
        RasLoc = 'RasLoc' + str(RNumber)
        RasImageLoction = Raspberry[RasLoc]
        RasOff = 'RasOff' + str(RNumber)
        RasImageOffset = Raspberry[RasOff]
        #
        NewLocation = RasImageLoction.move(RasImageOffset)
        #
        Raspberry[RasLoc] = NewLocation

        # Keep Raspberries on screen
        if NewLocation.left < 0 or NewLocation.right > ScreenWidth:
            NewOffset = -RasImageOffset[0]
            if NewOffset < 0:
                NewOffset = NewOffset -1
            else:
                NewOffset = NewOffset + 1
            RasImageOffset = [NewOffset, RasImageOffset[1]]
            Raspberry[RasOff] = RasImageOffset
        if NewLocation.top < 0 or NewLocation.bottom > ScreenHeight:
            NewOffset =- RasImageOffset[1]
            if NewOffset < 0:
                NewOffset = NewOffset -1
            else:
                NewOffset = NewOffset + 1
            RasImageOffset = [RasImageOffset[0], NewOffset]
            Raspberry[RasOff] = RasImageOffset
        GameScreen.blit(GameImageGraphic, NewLocation)
    pygame.display.update()