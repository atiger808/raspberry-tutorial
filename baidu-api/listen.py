# _*_ coding: utf-8 _*_
# @Time     : 2019/10/2 20:09
# @Author   : Ole211
# @Site     : 
# @File     : listen.py    
# @Software : PyCharm
'''
语音识别功能模块（语音输入）
参考：http://open.duer.baidu.com/doc/dueros-conversational-service/device-interface/voice-input_markdown

转换命令示例: wav, mp3, 转pcm文件
  1. wav 文件转 16k 16bits 位深的单声道pcm文件:
ffmpeg -y  -i 16k.wav  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 16k.pcm

  2.44100 采样率 单声道 16bts pcm 文件转 16000采样率 16bits 位深的单声道pcm文件:
ffmpeg -y -f s16le -ac 1 -ar 44100 -i test44.pcm  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 16k.pcm

  3.mp3 文件转 16K 16bits 位深的单声道 pcm文件:
ffmpeg -y  -i aidemo.mp3  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 16k.pcm
'''

from get_access_token import get_access_token
import os
import sys
import json
import base64
import time

IS_PY3 = sys.version_info.major == 3

if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode
    timer = time.perf_counter
else:
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import URLError
    from urllib import urlencode
    if sys.platform == "win32":
        timer = time.clock
    else:
        # On most other platforms the best timer is time.time()
        timer = time.time

# 1537 表示识别普通话，使用输入法模型。1536表示识别普通话，使用搜索模型。p根据文档填写PID，选择语言及识别模型
# 搜索模型： 1536 效果同手机百度搜索的语音输入。适合于短语识别，没有逗号。
# 输入法模型：1537 效果同百度输入法的语音输入。适合于长句识别，有逗号。
DEV_PID = 1537
token = get_access_token()
# 设置音频属性， 根据百度要求， 采样率必须为8000, 压缩格式支持pcm(不压缩), wav, opus, speex, amr
VOICE_RATE = 16000
wav_file = "auido.wav" #音频文件路径
USER_ID = 'ole211' # 用于标识的ID， 可以随意设置
WAVE_TYPE = "pcm"


def listen(wav_file):
    wav2pcm_file = wav_file.replace("wav", "pcm")
    os.system('ffmpeg -y  -i %s  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 %s'%(wav_file, wav2pcm_file))
    # 打开音频文件， 并进行编码
    with open(wav2pcm_file, 'rb') as speech_file:
        speech_data = speech_file.read()
    length = len(speech_data)
    speech = base64.b64encode(speech_data)
    if IS_PY3:
        speech = str(speech, 'utf-8')

    post_data = json.dumps({
        'dev_pid': DEV_PID,
        'format': WAVE_TYPE, 
        'rate':VOICE_RATE, 
        'channel':1, 
        'cuid':USER_ID, 
        'token':token, 
        'speech':speech, 
        'len':length
        }, sort_keys=False).encode('utf-8')
    url = 'http://vop.baidu.com/server_api'
    req = Request(url, post_data)
    req.add_header('Content-Type', 'application/json')
    try:
        f = urlopen(req)
        result_str = f.read()
    except URLError as err:
        print('http reponse error....', err.code)
    if IS_PY3:
        result_str = str(result_str, 'utf-8')
 
    result = json.loads(result_str)
    print("#"*30)
    print(result)
    if "success" in result['err_msg']:
        command = result['result'][0].encode('utf-8').decode()
        return command
    else:
        return '我没听懂你说什么'


if __name__ == '__main__':
    result = listen(input_file)
    print(result)



