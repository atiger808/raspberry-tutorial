from aip import AipSpeech
import sys, time

APP_ID = '17413508'
API_KEY = 'crxCtxVjGgPcHxwUcYEMoyws'
SECRET_KEY = 'SBdNH6ZHHpqdNw5kobNI4w2lslAgjQUS'
# 初始化
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


def text2sound(words='你好！', file_path='test.wav'):
    # 语音合成函数
    result = client.synthesis(words, 'zh', 1, {'per': 4, 'vol': 5, 'aue': 6, 'spd': 5, 'pit': 5})
    if not isinstance(result, dict):
        with open(file_path, 'wb') as f:
            f.write(result)
        return True
    else:
        return False


def sound2text(file_path='test.wav'):
    # 语音识别函数
    with open(file_path, 'rb') as fp:
        recog = client.asr(fp.read(), 'wav', 16000, {'dev_pid': 1537})
        if recog['err_no'] == 0:
            return recog['result'][0]


now = '你好主人，我是一个可爱的机器人，现在是北京时间: ' + time.strftime('%Y年 %m月 %d日 %H时 %M分 %S秒', time.localtime()) + "，你有什么问题可以问我"
msg = '主人好，今天您起色不错！'
text2sound(msg, file_path='./voice/door_praise.wav')
print('ok')
# r = sound2text('test.wav')
# print(r)
