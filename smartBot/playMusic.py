# _*_ coding: utf-8 _*_
# @Time     : 2019/10/15 2:03
# @Author   : Ole211
# @Site     : 
# @File     : playMusic.py    
# @Software : PyCharm

import os

def playMusic(music_path):
    os.system('mplayer '+music_path)