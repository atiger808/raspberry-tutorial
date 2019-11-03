# coding=utf-8
import sys
import requests
import json
import urllib.request

API_KEY = {
    "001":"c2d277352ca94610bf2b914979b08aa1",
    "002":'8bc5c23fad754947a4708721cffd759b',
    "003":"ab139f33beb3469fa2b937480f481cef",
    "004":"2e0c418b975c41beadb8f031b0642bf7",
    "005":"9b4469030aec4fe98a2ccc288342463f"
  }
USER_ID = 'Bot'
def tuling(words):
    api_url ="http://openapi.tuling123.com/openapi/api/v2"
    headers = {'Content-Type': 'application/json'}
    req = {
            "reqType": 0,  # 输入类型 0-文本, 1-图片, 2-音频
            "perception":  # 信息参数
            {
                "inputText":  # 文本信息
                {
                    "text": words
                },
 
                "selfInfo":  # 用户参数
                {
                    "location":
                    {
                        "city": "许昌",  # 所在城市
                        "province": "河南",  # 省份
                        "street": "文峰路"  # 街道
                    }
                }
            },
            "userInfo":
            {
                "apiKey": API_KEY["002"],  # 改为自己申请的key
                "userId": USER_ID  # 用户唯一标识(随便填, 非密钥)
            }
        }
    # 将字典格式的req编码为utf8
    req = json.dumps(req).encode('utf8')
    res = requests.post(api_url, data=req, headers=headers, verify=True).text
    if res:
        result = json.loads(res)
        print(result)
        result = result['results'][-1]['values']['text']
        return result
    else:
        return '我没有听懂哦'
        
if __name__ == '__main__':
    reply = tuling(sys.argv[1])
    print(reply)
