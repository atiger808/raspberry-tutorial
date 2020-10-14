# _*_ coding: utf-8 _*_
# @Time     : 2019/11/3 19:54
# @Author   : Ole211
# @Site     : 
# @File     : ipProxies.py    
# @Software : PyCharm

import requests, threading, datetime
from bs4 import BeautifulSoup as bs
import random, time


def write(path, ip):
    with open(path, 'a', encoding='utf-8') as f:
        f.writelines(ip)
        f.write('\n')


def truncatefile(path):
    with open(path, 'w', encoding='utf-8') as f:
        f.truncate()


def read(path):
    with open(path, 'r', encoding='utf-8') as f:
        txt = []
        for s in f.readlines():
            txt.append(s.strip())
    return txt


def runtime(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        print('start time: {}'.format(time.strftime('%Y-%m-%d %H:%M:%S')))
        back = func(*args, **kwargs)
        end = time.time()
        print('end time: {}'.format(time.strftime('%Y-%m-%d %H:%M:%S')))
        print('run time: %.2f' % (end - start))
        return back

    return wrapper


def gettimediff(start, end):
    seconds = (end - start).seconds
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    diff = ('%02d:%02d:%02d' % (h, m, s))
    return diff


def getheaders():
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1", \
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
    UserAgent = random.choice(user_agent_list)
    headers = {'User-Agent': UserAgent}
    return headers


def checkip(targeturl, ip):
    headers = getheaders()
    proxies = {'http': 'http://' + ip, 'https': 'https://' + ip}
    try:
        res = requests.get(targeturl, proxies=proxies, headers=headers, timeout=5)
        if res.status_code == 200:
            return True
        else:
            return False
    except:
        return False


def findip(type_id, pagenum, targeturl, path):
    'http://www.cnblogs.com/TurboWay/'  # 验证ip有效性的指定url
    type_list = {'1': 'http://www.xicidaili.com/nt/',  # xicidaili国内普通代理
                 '2': 'http://www.xicidaili.com/nn/',  # xicidaili国内高匿代理
                 '3': 'http://www.xicidaili.com/wn/',  # xicidaili国内https代理
                 '4': 'http://www.xicidaili.com/wt/'}  # xicidaili国外http代理
    url = type_list[str(type_id)] + str(pagenum)
    headers = getheaders()
    html = requests.get(url, headers=headers, timeout=5).text
    soup = bs(html, 'html.parser')
    all = soup.findAll('tr', class_='odd')
    for i in all:
        t = i.findAll('td')
        ip = t[1].text + ':' + t[2].text
        is_avail = checkip(targeturl, ip)
        if is_avail == True:
            write(path, ip)
            print(ip)


@runtime
def getip(targeturl, path):
    truncatefile(path)
    threads = [threading.Thread(target=findip, args=(type_id + 1, pagenum + 1, targeturl, path)) for type_id in range(4)
               for pagenum in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    ips = read(path)
    print('一共爬取代理ip: %s个' % (len(ips)))


if __name__ == '__main__':
    path = './ip_2.txt'
    targeturl = 'http://www.baidu.com'
    getip(targeturl, path)
