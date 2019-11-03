# _*_ coding: utf-8 _*_
# @Time     : 2019/10/2 20:51
# @Author   : Ole211
# @Site     : 
# @File     : speech.py    
# @Software : PyCharm
"""
语音转文字模块
"""


import os
import sys
import time
from imp import reload
reload(sys)

def say(what):
    from aip import AipSpeech
    '''你的 APPID AK SK'''
    APP_ID = '17413508'
    API_KEY = 'crxCtxVjGgPcHxwUcYEMoyws'
    SECRET_KEY = 'SBdNH6ZHHpqdNw5kobNI4w2lslAgjQUS'
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    result = client.synthesis(what, 'zh', 1, {
        # 发音人选择, 基础音库：0为度小美，1为度小宇，3为度逍遥，4为度丫丫，
# 精品音库：5为度小娇，103为度米朵，106为度博文，110为度小童，111为度小萌，默认为度小美 
        'per': 4, # 音库
        'spd': 4, # 语速
        'pit': 5, # 音调
        'vol': 5  # 音量
    })
    print(result)
    # 识别正确返回语音二进制， 错误则返回dict 参照下面错误码
    output_file = "say"+".wav"
    if not isinstance(result, dict):
        with open(output_file, 'wb') as f:
            f.write(result)
            print('ok')
    os.system('mpg123 /home/pi/raspberry-tutorial/smartBot/' + output_file)

if __name__ == '__main__':
    now = '你好主人，我是一个可爱的机器人，现在是北京时间: ' + time.strftime('%Y年 %m月 %d日 %H时 %M分 %S秒', time.localtime())
    msg = "，你有什么问题可以问我"
    say(now+msg)
