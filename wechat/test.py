# _*_ coding: utf-8 _*_
# @Time     : 2019/10/2 18:07
# @Author   : Ole211
# @Site     : 
# @File     : test.py    
# @Software : PyCharm

import itchat
from itchat.content import *

@itchat.msg_register(TEXT)
def simple_reply(msg):
    print(msg.text)

itchat.auto_login(hotReload=True)
itchat.run()