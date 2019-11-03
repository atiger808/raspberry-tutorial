
# _*_ coding: utf-8 _*_
# @Time     : 2019/10/16 3:32
# @Author   : Ole211
# @Site     : 
# @File     : human_infrare.py    
# @Software : PyCharm
from wxpy import *
import picamera
import time
import  RPi.GPIO as GPIO
#初始化
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12,GPIO.IN)
bot = Bot()
my_friend = bot.friends().search(u'道法自然')[0]
tuling = Tuling(api_key='8edce3ce905a4c1dbb965e6b35c3834d')
# 自动回复
@bot.register(msg_types=TEXT)
def auto_reply_all(msg):
    if GPIO.input(12) == True:
        #初始化照相机
        camera = picamera.PiCamera()
        camera.led = True
        try:
            #捕获图像
            camera.vflip = True
            camera.capture('image.jpg')
        except:
            my_friend.send('PiCamera Error')
        else:
            my_friend.send_image('image.jpg')
        finally:
            camera.close()
    else:
        tuling.do_reply(msg)
    time.sleep(5)
# 开始运行
time.sleep(5)
bot.join()