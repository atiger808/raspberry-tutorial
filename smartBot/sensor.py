# coding=utf-8
from config import TRIG_PIN, ECHO_PIN
from tuling import tuling
from speech import text2sound, sound2text
from record import record_sound, play_sound
from send_qq_img_email import send_img
import threading
import RPi.GPIO as GPIO
import time, random
import os



def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)

def checkdist():
    GPIO.output(TRIG_PIN, 0)
    time.sleep(0.000002)
    
    GPIO.output(TRIG_PIN, 1)
    time.sleep(0.000015)
    GPIO.output(TRIG_PIN, 0)
    
    while GPIO.input(ECHO_PIN) ==0:
        pass
    t1 = time.time()
    while GPIO.input(ECHO_PIN) ==1:
        pass
    t2 = time.time()
    return (t2-t1)*340/2

def asyn(f):
    def wrapper(*args, **kwargs):
        thr = threading.Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper

@asyn
def chat():
    # play_sound(file_path='sayHi.wav')
    while True:
        try:
            record_sound()
            text = sound2text()
            print('我  : %s' % text)
            # monitor(text)
            reply = tuling(text)
            print('机器人: %s' % reply)
            text2sound(reply)
            play_sound()
        except:
            pass

def sensor():
    current_state = 0
    previous_state = 0
    chat()
    while True:
        try:
            dist = checkdist()
            print(dist)
            current_state = 1 if dist<0.45 else 0
            if current_state == 1 and previous_state == 0:
                print('-----------有人----------')
                door_voice_path = ['./voice/door.wav', './voice/door_sayhi.wav', './voice/door_praise.wav']
                play_sound(file_path=random.choice(door_voice_path))
                previous_state = 1
            elif current_state == 0 and previous_state == 1:
                print('------------没人----------')
                play_sound(file_path='./voice/door_away.wav')
                previous_state = 0
            time.sleep(0.2)
        except:
            pass

if __name__ == '__main__':
    setup()
    sensor()
    print(checkdist())

