# _*_ coding: utf-8 _*_
# @Time     : 2019/11/3 19:09
# @Author   : Ole211
# @Site     : 
# @File     : doubanCrawl.py    
# @Software : PyCharm

from bs4 import BeautifulSoup as bs
import requests
import time, datetime
import json
import random
import os


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


headers1 = {
    'Host': 'movie.douban.com',
    'Referer': 'https://movie.douban.com/explore'
}


class Douban_DB(object):
    def __init__(self):
        self.conn = None

    def create_db(self):
        self.conn = sqlite3.connect('d:/hk_test.db')
        # 创建 hikvison 表
        self.conn.execute("""
        create table if not exists hk_test (
        id INTEGER PRIMARY KEY,
        date DATE DEFAULT NULL,
        title varchar DEFAULT NULL,
        counts INTEGER DEFAULT NULL,
        content varchar DEFAULT NULL,
        url varchar DEFAULT NULL)
        """)

    def save_db(self, dic):
        if dic:
            data = (dic['url_id'], dic['date'], dic['title'], dic['updatehit_counts'], dic['content'], dic['url'])
            insert_hikvision_cmd = "insert or replace into hk_test (id, date, title, counts, content, url) values (?, ?, ?, ?, ?, ?)"
            self.conn.execute(insert_hikvision_cmd, data)
            self.conn.commit()
            self.conn.close()
            print('Save db Success')
        else:
            print('Empty data')


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


def read():
    with open('d:/csv/ip_.txt', 'r', encoding='utf-8') as f:
        txt = []
        for s in f.readlines():
            txt.append(s.strip())
    return txt


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


def parse(url):
    headers = getheaders()
    headers.update(headers1)
    ip_list = read()
    random.shuffle(ip_list)
    for ip in ip_list:
        try:
            if checkip(url, ip) == True:
                proxies = {'http': 'http://' + ip, 'https': 'https://' + ip}
                res = requests.get(url, proxies=proxies, headers=headers, timeout=5)
                if res.status_code == 200:
                    return res.text
                else:
                    return None
        except Exception as e:
            print(e)
            continue


def save_json(dic, tag):
    if dic:
        with open(tag + '.json', 'a', encoding='utf-8') as f:
            content = json.dumps(dic, ensure_ascii=False) + '\n'
            f.write(content)


def get_tags():
    tagUrl = 'https://movie.douban.com/j/search_tags?type=movie&source='
    res = parse(tagUrl)
    if res:
        return json.loads(res)['tags']
    return None


def get_movie_info(movieUrl):
    html = parse(movieUrl)
    soup = bs(html, 'html.parser')
    li = soup.findAll('div', id='info')[0].text.strip().split('\n')
    li = [[i.split(':')[0].strip(), i.split(':')[1].strip()] for i in li]
    dic = {}
    for i in li:
        dic[i[0]] = i[1]
    return dic


def load_one_page(url, tag):
    data = json.loads(parse(url))
    if data.get('subjects'):
        for i in data['subjects']:
            try:
                dic = {}
                for k, v in i.items():
                    dic[k] = v
                dic['info'] = get_movie_info(dic['url'])
                dic.update(dic['info'])
                save_json(dic, tag)
                print(dic['title'])
            except:
                continue


def main(offset, tag):
    limit = 20
    page_start = 20
    for i in range(offset):
        url = 'https://movie.douban.com/j/search_subjects?type=movie&tag={}&page_limit={}0&page_start={}'.format(tag,
                                                                                                                 limit,
                                                                                                                 page_start * i)
        load_one_page(url, tag)


@runtime
def enter():
    if not os.path.exists('d:/csv/豆瓣电影'):
        os.makedirs('d:/csv/豆瓣电影')
    os.chdir('d:/csv/豆瓣电影')
    tags = ['热门', '最新', '经典', '可播放', '豆瓣高分', '冷门佳片', '华语', '欧美', '韩国', '日本', '动作', '喜剧', '爱情', '科幻', '悬疑', '恐怖', '文艺']
    for tag in tags:
        try:
            main(10, tag)
        except:
            continue


if __name__ == '__main__':
    enter()
