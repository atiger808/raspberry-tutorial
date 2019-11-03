# coding=utf-8
from config import TRIG_PIN, ECHO_PIN
from tuling import tuling
from speech import text2sound, sound2text
from record import record_sound, play_sound
from send_qq_img_email import send_img
import threading
import multiprocessing
import random
import os
import config as c
import RPi.GPIO as gpio
import importlib
import time


def asyn(f):
    def wrapper(self, *args, **kwargs):
        # thr = threading.Thread(target=f, args=args, kwargs=kwargs)
        thr = multiprocessing.Process(target=f, args=(self,))
        thr.start()

    return wrapper


class Bot():
    def __init__(self, r_pin, g_pin, b_pin, trig_pin, echo_pin, buzzer_pin, infrared_pin):
        gpio.setmode(gpio.BCM)
        self.r = r_pin
        self.g = g_pin
        self.b = b_pin
        self.trig = trig_pin
        self.echo = echo_pin
        self.buzzer = buzzer_pin
        self.infrared = infrared_pin
        self.tulingReply = True
        self.onLed = True

        gpio.setup(r_pin, gpio.OUT)
        gpio.setup(g_pin, gpio.OUT)
        gpio.setup(b_pin, gpio.OUT)
        gpio.setup(trig_pin, gpio.OUT)
        gpio.setup(echo_pin, gpio.IN)
        gpio.setup(buzzer_pin, gpio.OUT)
        gpio.output(buzzer_pin, gpio.HIGH)
        gpio.setup(infrared_pin, gpio.IN)

    def rgb(self, red=False, green=False, blue=False, delay=0.1):
        gpio.output(self.r, red)
        gpio.output(self.g, green)
        gpio.output(self.g, blue)
        time.sleep(delay)

    @asyn
    def bright_on(self):
        for i in range(5000):
            self.rgb(red=True)
            self.rgb(green=True)
            self.rgb(blue=True)
            self.rgb(red=True, green=True)
        self.bright_off()

    @asyn
    def bright_off(self):
        self.rgb()

    @asyn
    def take_picture(self):
        try:
            if not os.path.exists('./image/'):
                os.mkdir('./image/')
            os.system('sudo raspistill -o ./image/image.jpg -w 1024 -h 768 -t 2000')
            send_img('./image/')
        except:
            pass

    def checkdist(self):
        gpio.output(self.trig, 0)
        time.sleep(0.000002)

        gpio.output(self.trig, 1)
        time.sleep(0.000015)
        gpio.output(self.trig, 0)
        while gpio.input(self.echo) == 0:
            pass
        t1 = time.time()
        while gpio.input(self.echo) == 1:
            pass
        t2 = time.time()
        return (t2 - t1) * 340 / 2

    @asyn
    def ultrasonic_on(self):
        while True:
            dist = self.checkdist()
            print('------------- Distance: %.3f m --------------' % (dist))
            if dist < 0.4:
                self.rgb(red=True)
                for i in range(0, 3):
                    self.beep(0.25)
                text2sound('亲，我们靠的太近了,离我有%.3f 公分' % (dist * 100), file_path='temp.wav')
                play_sound(file_path='temp.wav')
                time.sleep(1)
            else:
                self.rgb(blue=True)
            time.sleep(0.1)

    @asyn
    def infrared_detect(self):
        while True:
            if gpio.input(self.infrared) == True:
                print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '-------Someone is here!!!')
                self.rgb(green=True)
            else:
                print('---------Infrared is Detecting-----------')
                self.rgb(green=False)
                time.sleep(0.1)

    def buzzer_on(self):
        GPIO.output(self.buzzer, GPIO.LOW)

    def buzzer_off(self):
        GPIO.output(self.buzzer, GPIO.HIGH)

    def beep(self, x):
        self.buzzer_on()
        time.sleep(x)
        self.buzzer_off()
        time.sleep(x)

    def playMusic(self, music_path):
        os.system('mplayer ' + music_path)

    def destroy(self):
        gpio.cleanup()

    def monitor(self, status):
        if status is not None:
            if ('跑马灯' in status and 'LED' in status) or '开灯' in status:
                play_sound(file_path='./voice/open_led.wav')
                self.rgb()
                self.bright_on()
                print('LED灯已经打开')
                self.tulingReply = False
                self.onLed = False
            elif u'关灯' in status or '关闭LED灯' in status:
                play_sound(file_path='./voice/shut_led.wav')
                self.destroy()
                print('LED灯已经关闭')
                self.tulingReply = False
            elif '红' in status:
                self.rgb(red=True)
                self.tulingReply = False
                self.onLed = False
            elif '绿' in status:
                self.rgb(green=True)
                self.tulingReply = False
                self.onLed = False
            elif '蓝' in status:
                self.rgb(blue=True)
                self.tulingReply = False
                self.onLed = False
            elif u'打开超声波' in status:
                play_sound(file_path='./voice/open_ultrasonic.wav')
                self.ultrasonic_on()
                self.tulingReply = False
            elif u'关闭超声波' in status:
                play_sound(file_path='./voice/shut_ultrasonic.wav')
                self.buzzer_off()
                print('超声波已经关闭')
                self.tulingReply = False
            elif '打开' in status and '红外线' in status:
                play_sound(file_path='./voice/open_infrared.wav')
                self.infrared_detect()
                self.tulingReply = False
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
                        self.playMusic(music)
                self.tulingReply = False
            elif u'拍张照片' in status or u'再来一张' in status:
                play_sound(file_path='./voice/camera.wav')
                self.take_picture()

                play_sound(file_path='./voice/send_success.wav')
                self.tulingReply = False
            elif '关机' in status:
                play_sound(file_path='./voice/shutdown.wav')
                self.tulingReply = False
                os.system('sudo poweroff')

            elif '重启' in status:
                play_sound(file_path='./voice/reboot.wav')
                self.tulingReply = False
                os.system('sudo reboot')

    @asyn
    def chat(self):
        now = '你好主人，我是一个可爱的机器人，现在是北京时间: ' + time.strftime('%Y年 %m月 %d日 %H时 %M分 %S秒', time.localtime()) + "，你有什么问题可以问我"
        text2sound(now)
        play_sound()
        while True:
            try:
                self.tulingReply = True
                self.onLed = True
                print('-Record Begin-')
                record_sound()
                text = sound2text()
                print('我  : %s' % text)
                self.monitor(text)
                if self.onLed == True:
                    self.rgb(green=True)
                if self.tulingReply == True:
                    reply = tuling(text)
                    print('机器:%s' % reply)
                    text2sound(reply)
                    play_sound()
            except:
                pass

    def sensor(self):
        current_state = 0
        previous_state = 0
        while True:
            try:
                # 超声波感应距离
                dist = self.checkdist()
                print('Distance: %.3f m' % dist)
                current_state = 1 if dist < 0.5 else 0
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
                    # if 3 >dist > 0.:
                    # play_sound(file_path='./voice/door_away.wav')
                    previous_state = 0
                time.sleep(0.2)
            except:
                pass


def main():
    bot = Bot(c.R_PIN, c.G_PIN, c.B_PIN, c.TRIG_PIN, c.ECHO_PIN, c.ACTIVE_BUZZER_PIN, c.INFRARED_PIN)
    msg = '机器人上线了....'
    # 红外感应打开
    # on_infrared()
    # 聊天模式打开
    bot.chat()


if __name__ == '__main__':
    time.sleep(5)
    main()
