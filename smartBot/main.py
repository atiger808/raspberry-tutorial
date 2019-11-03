# coding=utf-8
from config import TRIG_PIN, ECHO_PIN
from tuling import tuling
from speech import text2sound, sound2text
from record import record_sound, play_sound
from send_qq_img_email import send_img
from playMusic import playMusic
import threading
import multiprocessing
import random
import os

import RPi.GPIO as GPIO
import importlib
import time

R = 22
G = 23
B = 24
Buzzer_active = 17
Buzzer_passive = 16
TRIG = 19
ECHO = 20
Infrared = 5
color = {'Red': 0x00FFFF, 'Green': 0xFF00FF, 'Blue': 0xFF0000}
# monitor = importlib.import_module('35_temp_monitor')
# 有源蜂鸣
beep_active = importlib.import_module('10_active_buzzer')
# 无源蜂鸣
beep_passive = importlib.import_module('10_passive_buzzer')
# rgb LED 灯
rgb = importlib.import_module('02_rgb_led')
rgb2 = importlib.import_module('rgb_led')
# 超声雷达测距
ultrasonic = importlib.import_module('25_ultrasonic_ranging')
# 人体红外传感器
infrared = importlib.import_module('36_human_infrared')



# beep_active.setup(Buzzer_active)
# beep_passive.setup(Buzzer_passive)
# rgb.setup(R, G, B)
# rgb2.setup(R, G, B)
# ultrasonic.setup(TRIG, ECHO)
# infrared.setup(Infrared, R, G, B)

def setup():
    beep_active.setup(Buzzer_active)
    # beep_passive.setup(Buzzer_passive)
    rgb2.setup(R, G, B)
    ultrasonic.setup(TRIG, ECHO)
    infrared.setup(Infrared, R, G, B)
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)


def destroy():
    beep_active.destroy()
    # beep_passive.destroy()
    rgb.destroy()
    ultrasonic.destroy()
    infrared.destroy()
    GPIO.cleanup()


def asyn(f):
    def wrapper(*args, **kwargs):
        thr = threading.Thread(target=f, args=args, kwargs=kwargs)
        #thr = multiprocessing.Process(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper


#@asyn
def on_music(music):
    print('————- 开始播放音乐！————-')
    playMusic(music)
    print('————- 音乐播放完毕！————-')


@asyn
def on_ultrasonic():
    setup()
    while True:
        dist = ultrasonic.distance()
        print('------------- Distance: %.3f m --------------' % (dist))
        if dist < 0.4:
            rgb.setColor(color['Red'])
            for i in range(0, 3):
                beep_active.beep(0.25)
            text2sound('亲，我们靠的太近了,离我有%.3f 公分' % (dist * 100), file_path='temp.wav')
            play_sound(file_path='temp.wav')
            time.sleep(1)
        else:
            rgb.setColor(color['Blue'])
        time.sleep(0.1)


@asyn
def on_ultrasonic2():
    os.system('python ./35_temp_monitor.py')


@asyn
def on_bright():
    rgb2.setup(R, G, B)
    for i in range(2000):
        rgb2.bright()
    rgb2.destroy()

@asyn
def on_infrared():
    rgb2.setup(R, G, B)
    infrared.setup(Infrared, R, G, B)
    infrared.detect()


def checkdist():
    GPIO.output(TRIG_PIN, 0)
    time.sleep(0.000002)

    GPIO.output(TRIG_PIN, 1)
    time.sleep(0.000015)
    GPIO.output(TRIG_PIN, 0)

    while GPIO.input(ECHO_PIN) == 0:
        pass
    t1 = time.time()
    while GPIO.input(ECHO_PIN) == 1:
        pass
    t2 = time.time()
    return (t2 - t1) * 340 / 2

@asyn
def take_picture():
    if not os.path.exists('./image/'):
        os.mkdir('./image/')
    os.system('sudo raspistill -o ./image/image.jpg -w 1024 -h 768 -t 2000')
    send_img('./image/')

def monitor(status):
    if status is not None:
        global tulingReply
        if ('打开' in status and 'LED' in status) or '开灯' in status:
            play_sound(file_path='./voice/open_led.wav')
            on_bright()
            print('LED灯已经打开')
            tulingReply = False
            onLed = False
        elif u'关灯' in status or '关闭LED灯' in status:
            play_sound(file_path='./voice/shut_led.wav')
            rgb2.destroy()
            print('LED灯已经关闭')
            tulingReply = False
        elif u'打开超声波' in status:
            play_sound(file_path='./voice/open_ultrasonic.wav')
            on_ultrasonic2()
            tulingReply = False
        elif u'关闭超声波' in status:
            play_sound(file_path='./voice/shut_ultrasonic.wav')
            destroy()
            print('超声波已经关闭')
            tulingReply = False
        elif '打开' in status and '红外线' in status:
            play_sound(file_path='./voice/open_infrared.wav')
            tulingReply = False
        elif u'音乐' in status or u'歌曲' in status or u'再来一首' in status or u'music' in status:
            file_path = '/home/pi/Music/'
            if os.path.isdir(file_path):
                music_path = [os.path.join(file_path, i) for i in os.listdir(file_path)]
                music_name = [os.path.split(i)[-1].split('.')[0] for i in music_path]
            play_sound(file_path='./voice/playmusic.wav')
            song = random.choice(music_name)
            text2sound('一首' + song + '送个你')
            play_sound()
            for music in music_path:
                if song in music:
                    on_music(music)
            self.tulingReply = False
        elif u'拍张照片' in status or u'再来一张' in status:
            play_sound(file_path='./voice/camera.wav')
            take_picture()
            play_sound(file_path='./voice/send_success.wav')
            tulingReply = False
        elif '关机' in status:
            play_sound(file_path='./voice/shutdown.wav')
            tulingReply = False
            os.system('sudo poweroff')
  
        elif '重启' in status:
            play_sound(file_path='./voice/reboot.wav')
            tulingReply = False
            os.system('sudo reboot')

@asyn
def chat(msg):
    global tulingReply
    print(msg)
    while True:
        try:
            tulingReply= True
            onLed = True
            print('---------Record Begin-------------')
            record_sound()
            text = sound2text()
            print('我  : %s' % text)
            monitor(text)
            if onLed == True:
                rgb2.rgb(green=True)
            if tulingReply == True:
                reply = tuling(text)
                print('机器人: %s' % reply)
                text2sound(reply)
                play_sound()
        except:
            pass

def main():
    current_state = 0
    previous_state = 0
    msg = '机器人上线了....'
    # 红外感应打开
    # on_infrared()
    # 聊天模式打开
    chat(msg)
    while True:
        try:
            # 超声波感应距离
            dist = checkdist()
            print('Distance: %.3f m' %dist)
            current_state = 1 if dist<0.5 else 0
            if current_state == 1 and previous_state == 0:
                print('-----------有人----------')
                door_voice_path = ['./voice/door.wav', './voice/door_sayhi.wav', './voice/door_praise.wav']
                play_sound(file_path=random.choice(door_voice_path))
                time.sleep(random.randint(1, 4))
                play_sound(file_path='./voice/door_chat.wav')
                if dist < 0.3:
                    play_sound(file_path='./voice/door_nearest.wav')
                previous_state = 1
            elif current_state == 0 and previous_state == 1:
                print('------------没人----------')
                if 3 >dist > 0.:
                    play_sound(file_path='./voice/door_away.wav')
                previous_state = 0
            time.sleep(0.2)
        except:
            pass


if __name__ == '__main__':
    time.sleep(3)
    setup()
    # print(checkdist())
    main()