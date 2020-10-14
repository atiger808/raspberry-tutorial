# _*_ coding: utf-8 _*_
# @Time     : 2019/9/22 4:24
# @Author   : Ole211
# @Site     : 
# @File     : send_qq_img_video_email.py
# @Software : PyCharm

import traceback
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import random
import time
# from email.header import Header
# from email.utils import formataddr

username = "594542251@qq.com"  # qq账户
authorization_code = "agokwajqivckbdhg"  # qq邮箱授权码
from_email = "594542251@qq.com"


def send_qq_img_email(from_email, to_emails, title, content, attachname,  imgname):
    """04发送带有图片的html邮箱"""
    send_fail = []
    for to_email in to_emails:
        # 创建 一个带有图片的实例
        message = MIMEMultipart("reload")
        message['Subject'] = "{}".format(title)
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

        # 构造附件
        if (os.path.getsize(attachname)/1024) > 200:
            attach = MIMEText(open(attachname, 'rb').read(), 'base64', 'utf-8')
            attach["Content-Type"] = 'application/octet-stream'
            # filename 是邮件中显示的名字
            attach["Content-Disposition"] = 'attachment; filename={}'.format(attachname)
            message.attach(attach)
            print('{}------sending'.format(attachname))

        try:
            # 创建发送邮件对象
            print('-------sendmail-------')
            s = smtplib.SMTP_SSL("smtp.qq.com", 465)
            s.login(username, authorization_code)
            s.sendmail(from_email, to_email, message.as_string())
            s.quit()
            print('发送成功')
        except smtplib.SMTPException as e:
            send_fail.append(to_email)
            print("发送失败，%s" % e)
    return send_fail

def main():

    # to_emails = ['474336539@qq.com','594542251@qq.com', '407755963@qq.com', '985277476@qq.com', '1197773452@qq.com']
    # to_emails = ['594542251@qq.com', '407755963@qq.com', '1197773452@qq.com']
    to_emails = ['ole211@qq.com', '1197773452@qq.com']


    # 邮件附件文件名， 打开的是本目录文件
    attachs = []
    file_path = './record/'
    attachs = [os.path.join(file_path, i) for i in os.listdir(file_path)]

    # 发送带图片的文件内容
    img_content = """
                <h2>异常预警， 实时抓拍</h2>
                <p><img style="width: 640px; height: 480px;" src="cid:image_test"></p>

        """
    # 图片名称
    file_path = './image/'
    imgs = [os.path.join(file_path, i) for i in os.listdir(file_path)]

    if len(imgs)>0 or len(attachs)>0:
        for imgname in imgs:
            for attachname in attachs:
                if os.path.splitext(os.path.basename(imgname))[0].strip('_shoot') == os.path.splitext(os.path.basename(attachname))[0]:
                    try:
                        send_fail = send_qq_img_email("594542251@qq.com", to_emails, "有动静了o", img_content, attachname, imgname)
                        time.sleep(random.randint(1, 4))
                    except Exception as e:
                        print(e)
                        continue
                os.remove(imgname)
                os.remove(attachname)

    else:
        print('empty')
if __name__ == '__main__':
    while True:
        main()
        time.sleep(10)