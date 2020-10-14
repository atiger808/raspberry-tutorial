# _*_ coding: utf-8 _*_
# @Time     : 2020/4/28 11:21
# @Author   : Ole211
# @Site     : 
# @File     : theWorldDisease.py    
# @Software : PyCharm

import requests
import time
import pandas as pd
import json
# timestamp = int(time.time()*1000)
# real_url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_foreign&callback=&_=%d'%timestamp
# res = requests.get(real_url)
# data = res.json()
# # print(data['data'])
# dic_data = json.loads(data['data'])
# df = pd.DataFrame(dic_data['foreignList'])
# df.to_csv('theWorldDisease.csv')

from selenium import webdriver
from bs4 import BeautifulSoup as bs

executable_path = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe'
driver = webdriver.Chrome(executable_path=executable_path)
url = 'https://news.qq.com/zt2020/page/feiyan.htm#/global'
driver.get(url)
html = driver.page_source
print(html)


