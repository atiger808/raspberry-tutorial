# _*_ coding: utf-8 _*_
# @Time     : 2020/4/21 15:35
# @Author   : Ole211
# @Site     : 
# @File     : douyin.py    
# @Software : PyCharm


'''
  https://v.douyin.com/ThafwQ/
    https://v.douyin.com/ThAK7f/
      https://v.douyin.com/ThPhGq/
        https://v.douyin.com/TkdD8b/
      https://www.iesdouyin.com/share/user/50835769103    ?u_code=l971hl0h&sec_uid=MS4wLjABAAAA764K70gtV6Z7wmVSvaX42Qw1lbmxXm2srpggIkpiqAA&timestamp=1587398873&utm_source=copy&utm_campaign=client_share&utm_medium=android&share_app_name=douyin
'''

import requests, re, json, time

# from ipadress import ip_adress

rip = '10.208.222.88'
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Linux; U; Android 5.1.1; zh-cn; MI 4S Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/9.1.3',
    'X-Real-IP': str(rip),
    'X-Forwarded-For': str(rip),
}

url = 'https://v.douyin.com/TkjEJo/'
# url = 'https://www.iesdouyin.com/share/user/50835769103'
res = requests.get(url, headers=headers)
print(res.status_code)
print(res.text)
uid = re.search('uid: "(.*?)"', res.text).group(1)
dytk = re.search("dytk: '(.*?)'", res.text).group(1)
print(uid, dytk)
print(res.headers)
print(res.headers['location'])


params = {
    'user_id': uid,
    'count': '10',
    'max_cursor': '0',
    'aid': '1128',
    'dytk': dytk
}
#
# while True:
#     furl = 'https://www.iesdouyin.com/aweme/v1/aweme/favorite'
#     furl = 'https://www.douyin.com/aweme/v1/aweme/post/'
#     res = requests.get(furl, params=params, headers=headers, verify=False)
#     print(res.headers)
#     jsonstr = res.json()
#     print(jsonstr)
#     time.sleep(1)
#     aweme_list = jsonstr.get('aweme_list')
#     if len(aweme_list) != 0:
#         break
#
# for item in aweme_list:
#     video_id = item['video']
#     video_url = 'https://aweme.snssdk.com/aweme/v1/playwm/?video_id=' + video_id
#     video_title = item['share_info']['share_desc']
#     mp4 = requests.get(video_url, headers=headers, stream=True).content
#     with open(video_title + '.mp4', 'wb') as f:
#         f.write(mp4)
