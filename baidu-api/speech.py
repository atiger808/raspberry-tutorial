# _*_ coding: utf-8 _*_
# @Time     : 2019/10/2 20:51
# @Author   : Ole211
# @Site     : 
# @File     : speech.py    
# @Software : PyCharm

import os
import sys
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
        'vol': 5,
        'per': 3,
    })
    print(result)
    # 识别正确返回语音二进制， 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open('auido.mp3', 'wb') as f:
            f.write(result)
            print('ok')
    os.system('auido.mp3')

if __name__ == '__main__':
    say('大家好, 我是来自大墙王村的机器人小度')