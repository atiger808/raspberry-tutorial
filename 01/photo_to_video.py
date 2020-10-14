# _*_ coding: utf-8 _*_
# @Time     : 2019/10/8 23:07
# @Author   : Ole211
# @Site     : 
# @File     : photo_to_video.py    
# @Software : PyCharm

import os
import cv2

file_path = r'E:\images\family'
if os.path.isdir(file_path):
    imgs = [os.path.join(file_path, i) for i in os.listdir(file_path)]

for i in range(len(imgs)):
    frame = cv2.imread(imgs[i])
    frame = cv2.resize(frame, (640, 480), cv2.INTER_CUBIC)
    cv2.imshow('frame', frame)
    k = cv2.waitKey(20) & 0xff
    if k == 27:
        break
cv2.destroyAllWindows()