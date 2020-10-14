# _*_ coding: utf-8 _*_
# @Time     : 2019/10/2 19:48
# @Author   : Ole211
# @Site     : 
# @File     : get_access_token.py    
# @Software : PyCharm

import urllib.request
import sys
import json
import ssl

'''
# .百度账号:18668183817 API
APP_ID = "17516199"
API_KEY = "4cHuY83mlSV0k6pybfOyQSc3"
SECRET_KEY = "mFM5ydm42txh94Uehys0rZu69SN1nVuY"
'''
# 百度账号:594542251@qq.com API
APP_ID = '17413508'
API_KEY = 'crxCtxVjGgPcHxwUcYEMoyws'
SECRET_KEY = 'SBdNH6ZHHpqdNw5kobNI4w2lslAgjQUS'


def get_access_token():
    
    # client_id = 'a1oiSUfK3pmnUkay7zP5cbIy'
    # client_secret = 'yp6ogvjeZkoYBqLiB5UkWAyEpKKcgBdI'
    
    client_id = API_KEY
    client_secret = SECRET_KEY
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(client_id, client_secret)
    request = urllib.request.Request(host)
    request.add_header('Content-Type', 'application; charset=UTF-8')
    response = urllib.request.urlopen(request)
    content = response.read()
    if content:
        data = json.loads(content)
        return data['access_token']
    return None

if __name__ == '__main__':
    print(get_access_token())