# _*_ coding: utf-8 _*_
# @Time     : 2019/9/22 4:24
# @Author   : Ole211
# @Site     : 
# @File     : send_qq_img_email.py    
# @Software : PyCharm

import traceback
import os
import sys
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import time
from email.header import Header

# from email.utils import formataddr

username = "594542251@qq.com"  # qq账户
authorization_code = "agokwajqivckbdhg"  # qq邮箱授权码
from_email = '王先森<594542251@qq.com>'


def send_qq_img_email(from_email, to_emails, title, content, imgname):
    """04发送带有图片的html邮箱"""
    send_fail = []
    for to_email in to_emails:
        # 创建 一个带有图片的实例
        message = MIMEMultipart("reload")
        message['Subject'] = Header(title, 'utf-8')
        message['From'] = from_email
        message['To'] = to_email

        message_alternative = MIMEMultipart('alternative')
        message.attach(message_alternative)
        message_alternative.attach(MIMEText(content, "html", "utf-8"))

        # 打开图片
        image = open(imgname, 'rb')
        msgImage = MIMEImage(image.read())
        image.close()

        # 定义图片id, 在html文本中引用
        msgImage.add_header('Content-ID', '<image_test>')
        message.attach(msgImage)

        try:
            # 创建发送邮件对象
            print('-------sendmail-------')
            s = smtplib.SMTP_SSL("smtp.qq.com", 465)
            s.login(username, authorization_code)
            s.sendmail(from_email, to_email, message.as_string())
            s.quit()
            print('发送成功----{}'.format(to_email))
        except smtplib.SMTPException as e:
            send_fail.append(to_email)
            print("发送失败，%s" % e)
    return send_fail


def send_img(file_path):
    # to_emails = ['474336539@qq.com','ole211@qq.com', '407755963@qq.com', '985277476@qq.com']
    # to_emails = ['ole211@qq.com', '407755963@qq.com', '985277476@qq.com']
    # to_emails = ['ole211@qq.com', '1197773452@qq.com']
    to_emails = ['ole211@qq.com']

    # 发送带图片的文件内容
    img_content = """
                <h2>动态监测， 实时抓拍</h2>
                <p><img style="width: 640px; height: 480px;" src="cid:image_test"></p>

        """
    # 图片名称
    # file_path = './image/'
    if os.path.isdir(file_path):
        imgs = [os.path.join(file_path, i) for i in os.listdir(file_path)]
        if len(imgs) > 0:
            for imgname in imgs:
                try:
                    title = os.path.basename(imgname).strip('.jpg').replace('_', ':')
                    print(title)
                    send_fail = send_qq_img_email(from_email, to_emails, title, img_content, imgname)
                    time.sleep(random.randint(1, 4))
                    # os.remove(imgname)
                except Exception as e:
                    print(e)
                    continue
        else:
            print('empty')
    else:
        print('this dir is not exists')


if __name__ == '__main__':
    while True:
        send_img(sys.argv[1])
        time.sleep(3)
