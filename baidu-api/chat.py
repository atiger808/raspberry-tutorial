from speech import say
from listen import listen
import os, sys

def chat():
    wav_file = '/home/pi/raspberry-tutorial/baidu-api/temp.wav'
    msg = listen(wav_file)
    say(msg)
    print(msg)


chat()

