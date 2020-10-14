import requests
import json
from time import sleep
import random
from getheaders import getheaders
from run_time import run_time as run
import os, time
import threading



url = 'http://ywzs.jyt.henan.gov.cn/xxzs/BasicInfo/SaveStudent'
jumpUrl = 'http://ywzs.jyt.henan.gov.cn/xxzs/Account/Login?ReturnUrl=%2Fxxzs%2FBasicInfo%2FSaveStudent'

headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',

    'Cookie': 'cookie01=2.1c.61.cab82412.50; Hm_lvt_5288aab03e95c23535085e433fce1276=1595659269,1595659459,1595659541,1595661398; code=mH7D7O5vAFI%3D; c=3UyIZBxt34c%3D; xx=CfDJ8Fm7NrMhvXlOvG3aU2QSK8fIN92Yh84nLmmeHhFgZNclLfLc4GHgHc4G9BnLHy4MSWrQqNz-HOJ-jqGEm2usjQv735Svpkz-3FVpTGEhduDrfDL6-BuFNB_IJet90OEKv7w7lDihQJzZfcnIenHgveUYLyX3EmsOqoiLQWHa-n3fJfJtnu9aB2j5y-PqdC54sK7HiqMa3zYUn1sqC1Jio_jPGBA9sptdE3Z99MbES1rXR_CiERS3aTFwNhvBbYSlei_dwpgnHgtWXfGoolNCWV5otBCStQd5bsNB88H-x_gRoPE3B2bVlEce0PbWwKKIwhLxyNN0h9VTJhA6TDhPEMT8QGO2THBnU7AKSiQ2DB8IBt5t1cLywX40A4323HgVrxdV8Q6gWubNaj2HSS3PSJMWgQPQ0xy_YPXFrp7ZOg3tjFxSqw-irKV5tPdFN0ySvaMSD6nrbkhsPS6LC7CJ-PBJ_Fb-dRzxnRft7TEcl1U4Eyhnhdr03YUreWSc97VwIg; Hm_lpvt_5288aab03e95c23535085e433fce1276=1595710666',

    'Host': 'ywzs.jyt.henan.gov.cn',
    'Origin': 'http://ywzs.jyt.henan.gov.cn',
    'Referer': 'http://ywzs.jyt.henan.gov.cn/xxzs/BasicInfo/StuBasicInfo',
    'User-Agent': getheaders()['User-Agent']
}

data = {
    'PerfectStatus': '0',
    'gbm': '156',
    'pSchoolName': '任庄童星幼儿园',
    'birthday': '2014-06-06',
    'sfzjlxm': '1',
    'studentno': '',
    'entranceno': '4110030002509',
    'hjlxm': '222',
    'PQINFO': '4110030002509',
    'homeaddr': ' 建安区魏风路小学学区范围：东：学院路以西。西：仓库路以东。南：瑞贝卡大道以北。北：恒通路以南。以内的①翡翠花园②幸福花城③金质花园④南苑新城⑤宏安佳苑⑥玫瑰公寓⑦东源锦程⑧东源锦秀⑨天合丽景新苑⑩林润人和苑苑魏风路以西的防疫站家属院、农科所独院、联通五分公司等属建安区社区管理的家属院院招生范围内没有名称的老旧家属',
    'Province': '河南',
    'City': '许昌',
    'Country': '建安',
    'Polic': '灵井镇',
    'hjszd': '河南省许昌市建安县/区灵井镇派出所',
    'nowadd': '沟头刘村4组',
    'family': [
        {"JTGX": {"CODE": "2", "NAME": "母亲"}, "NAME": "洪艳秋", "PHONE": "15893742631", "IDNUMBER": "230822197909134948",
         "HJSZD": "河南省许昌县灵井镇沟头刘村4组", "WORKUNIT": "许昌市朝阳物业管理服务有限公司"}],
    'studentname': '刘家馨',
    'idcard': '411023201406060234',
    'extrainfor': {"XB": {"CODE": "1", "NAME": "男"}, "MZ": {"CODE": "01", "NAME": "汉族"}, "BIRTHDAY": "2014-06-06",
                   "SFZJLX": {"CODE": "1", "NAME": "居民身份证"}, "SCHOOLNAME": "许昌市建安区魏风路小学",
                   "GB": {"CODE": "156", "NAME": "中国"}, "HJLX": {"CODE": "222", "NAME": "随迁子女"},
                   "HJSZD": "河南省许昌市建安县/区灵井镇派出所", "HOMEADDR": {"CODE": "4110030002509",
                                                              "NAME": "建安区魏风路小学学区范围：东：学院路以西。西：仓库路以东。南：瑞贝卡大道以北。北：恒通路以南。以内的①翡翠花园②幸福花城③金质花园④南苑新城⑤宏安佳苑⑥玫瑰公寓⑦东源锦程⑧东源锦秀⑨天合丽景新苑⑩林润人和苑苑魏风路以西的防疫站家属院、农科所独院、联通五分公司等属建安区社区管理的家属院院招生范围内没有名称的老旧家属\u0000"},
                   "NOWADD": "沟头刘村4组", "PSCHOOLNAME": "任庄童星幼儿园"},
    'schoolid': '2020060118511236165696701',
    'stage': '1',  # 判断是否在截止日期内
    'PERFECTSTATUS': '1',
    'SCHOOLID': '2020060118511236165696701'
}


def read(path):
    with open(path, 'r', encoding='utf-8') as f:
        txt = []
        for s in f.readlines():
            txt.append(s.strip())
    return txt


def checkip(ip):
    targeturl = 'http://www.baidu.com'
    headers = getheaders()
    proxies = {'http': 'http://' + ip, 'https': 'https://' + ip}
    try:
        res = requests.get(targeturl, proxies=proxies, headers=headers, timeout=2)
        if res.status_code == 200:
            return True
        else:
            return False
    except:
        return False


@run
def reg(url, IP, flag=True):
    while True:
        ip = random.choice(ips3)
        try:
            proxies = {'http': 'http://' + ip, 'https': 'https://' + ip}
            if flag:
                res = requests.post(url, proxies=proxies, headers=headers, data=data, timeout=5)
            else:
                res = requests.post(url, headers=headers, data=data, timeout=5)
            print(res.status_code)
            print(res.url)

            # 如果服务器响应， 且cookie未过期
            if res.status_code == 200 and res.url != jumpUrl:
                print(res.text)
                r = json.loads(res.text)
                if r.get('code') == -1:
                    print('不在网上信息完善时间范围内不能保存！')
                    continue
                elif r.get('code') != '200':
                    continue
                else:
                    print('基本信息保存完成。!......')
                    print('success!')
                    base_dir = os.path.dirname(os.path.abspath(__file__))
                    os.system('python {} {}'.format(os.path.join(base_dir,'send_qq_img_email.py'), os.path.join(base_dir,'image')))
                    break

            # 如果cookie过期
            elif res.status_code == 200 and res.url == jumpUrl:
                print('cookie 过期')
                break
            else:
                continue

            # sleep((random.randint(10, 30))/10)
        except Exception as e:
            print('错误信息： %s \n' % e)
            continue


if __name__ == '__main__':
    dic = {
        'Cookie': 'cookie01=2.1c.61.cab82412.50; Hm_lvt_5288aab03e95c23535085e433fce1276=1595659269,1595659459,1595659541,1595661398; code=mH7D7O5vAFI%3D; c=odaBZTgrf0g%3D; Hm_lpvt_5288aab03e95c23535085e433fce1276=1595674055; xx=CfDJ8Fm7NrMhvXlOvG3aU2QSK8cNw5dTMn_WmLRZI6ABodeVGe35lll8FC35Ks-mpUN-A-G5dYMXILeR_tWsatmL7e-Hfz9owS6EcCXY5QtmpgbtvrqEeLqXUWsIEbfxiRp_gbDnsYmO-KTk1qlVoEunIct4Oh5CUiE7zi9Vy5yWjnz3uj9UdeONzsIG-v_6Cm-Irabt2i0XB-7O5W0acl6O2fUPTEzn7dyqYr_3ulAY2zHRra0T77bWbpzklxDEl_NnQ_-6q4aID6TkfGrENq5bbO2LLGUJAfIoMA1q8umgmZkOxd2nPkfcw-pbjVE5uKZgi0o92FBxmW6Gz97a6dmVSFZI6y94Z-o2nacamwFWnF0KRLA8IIZpmFuEPUYO8X-KwjWl07qU9X3stpCBZHzTFHNB5CVpaT4Df-9rl-knPMcAplCbWS9jyB6x_vFdHxE7JC0dJn68xGZvk2MQfCFgbJEs9TvJ-AsydlcmRGSEz19HlzjBTzZzNXVBWLniWXvyJQ',
        'Cookie': 'cookie01=2.1c.61.cab82412.50; Hm_lvt_5288aab03e95c23535085e433fce1276=1595659269,1595659459,1595659541,1595661398; code=mH7D7O5vAFI%3D; c=odaBZTgrf0g%3D; Hm_lpvt_5288aab03e95c23535085e433fce1276=1595674055; xx=CfDJ8Fm7NrMhvXlOvG3aU2QSK8ckSuP971--U02S7haCUJsbWWGlrOuj057Xtc9322KMw8WVny8zevI3p28JaerdqyFUyR8KGo-CrfSEXXuzKQLjDIG2NuQIN-Q_7wzlaZQ-qogP3oijM3_h68DzG18-8eQ5XWm9csbyxSpcQN5PkqPHhcmGUHk4WqhbLoHIOHt1_Bhj0O-6dAL8poA-lcWLQ46HdcuwB7Pwv87OsFoPMn204ee--rxuY7eRh2ojv3uob4LBkqY5oTmkZK3SCCJ0HmoHtxHeAiRACl07SfGjHJN4Shb78d4rt6EG8nx0mTntaPAy8sG4RuJHK0lovxi5xubA411f6ToNpcjazZDa8QmTYVAnhBJ6aZYxRLqm-C6mpVRhCrq3k1qkMCXZDwAdd3CN90mIRxzskzMU-O4j3F6xGx86txk518u2-5ZqHPt_JAcysJR2LRPnJT68tRFYrL3uiDjAo68cGxDcWbvMlKW4AFA3vpygGsPGXUdAsW77rw',
        'Cookie': 'cookie01=2.1c.61.cab82412.50; Hm_lvt_5288aab03e95c23535085e433fce1276=1595659269,1595659459,1595659541,1595661398; code=mH7D7O5vAFI%3D; c=odaBZTgrf0g%3D; xx=CfDJ8Fm7NrMhvXlOvG3aU2QSK8d5YacuiOClhJHwblltjufRryf_eyxHf-JT3OVSSPyJIYJFYi4nHTG-8ME0jZwNFTwirFdf39RsihwYuxjgpL3TJQaqy-ewRE07ZDLMO0nZw5485edGlk6uxZIFnrMlMkQq19vgTdeKvh5RQ8HSj_sDAX59ayt9o9vIS4_-cvAEQN-RR9tUuVWrIEhK9bQZ6VrbOCZFh9yY7mMkQD_hJl3Yz06iGN2B12C_vsYX-qzlSruXHdBOrMbmd7jE91ZAxDvzs44khs9AbyrEVxF-qu_6BgiL4rMbfafJVm0HyI50smfSMjX0Ccdqou8am-BS1krtXQPrOoPjfChUgov9g0Uvz_YZLyL-rpqFroCQ9ZKRdMTD0C4zWbRy7GETR9yuwJDl8ccwTzF9gYggDmxKVV1LeDph82TIbtPAgJkHJzKfuavPA0HpBlD7aFSEyApAGndwDt1nYs8OunNegDQGgwuf2tdmMjocDWHXsFx_IIuUtg; Hm_lpvt_5288aab03e95c23535085e433fce1276=1595684559',

        'Cookie': 'cookie01=2.1c.61.cab82412.50; Hm_lvt_5288aab03e95c23535085e433fce1276=1595659269,1595659459,1595659541,1595661398; code=mH7D7O5vAFI%3D; c=zkNnQVmuXng%3D; xx=CfDJ8Fm7NrMhvXlOvG3aU2QSK8cwAulpnEPeq-SPCQAkSh66a0N4v-OWh_CvhovpnENZA4pgNAPuw1Tpx1g-XzAcTqSuyj2HdjOb5DlFsF0HDG0x_RvU6YhKT81jn3le5UYywqpZdt1Ioo0PCXYnP3RPypE8MGe8OOe3B8NHtQykqi8fXikWbWR1UQqU9Kb0lBQ0Jtj9YZwKml9ptDdPzga5wbLdba-dUi6WxVS79_NW8vK7s3idGk9HMO9v3iwMIcH1f0GodfhlPc47Pson1pgqJ8UiXZ2UmY2XO2PuYYLRAki72UkI47F-rusWKKrinfvPy5vuPWAQfgyN8d6gF_TY3NN6NtL-27Wl1FMZEa9vu1io8ky65zIqO2veZ-Mb8TLMIjOhC52uxlgpK1TIFQHEv1N9w-FDqXxO92yYu4Fs_WfNceZu03AETVsoaDAnMQfJZbNL1SfwERHjBgMD9Zc1lcMjveeiiQXp7Q1pN1H60-ycfptf69SN9GQdCvdP1Mukrg; Hm_lpvt_5288aab03e95c23535085e433fce1276=1595688865',

        'Cookie': 'cookie01=2.1c.61.cab82412.50; Hm_lvt_5288aab03e95c23535085e433fce1276=1595659269,1595659459,1595659541,1595661398; code=mH7D7O5vAFI%3D; c=zkNnQVmuXng%3D; Hm_lpvt_5288aab03e95c23535085e433fce1276=1595688865; xx=CfDJ8Fm7NrMhvXlOvG3aU2QSK8cXPLFsjjrIvQVrUbBto3Fp3X2zP_xEwERwa4DjszdvCty8-OyTqcHgzbxsZuuS7eDoq8RRRZKXdAKc3ss8xd15LM_2vswnrMv-tm0ZZnBCUfFm0HBQNkRx06XCIFxbmJNSIOZuaI5xA4d_8U6h7tnI61w__cx55HMHetE6-rONiH8UlXO5FGGOx9dNBf5t6Dgyp31JD1WLn-nUMukFr8Vp9Zn5JAfUZ9S0Qx_TA3sW5qtL9o7E3YKzsLdYRtRv803TGMEWOfzohjnllW-84o3I0GuGVaDFgAhwVylNacfxWtoPc9LQWuW3DzEXeGdQ10VhU-v_1J0_TBZ1jfUpxDdRSTBnajZdrMRvBQc6z4x3KA4m0YV9kcu2k5GnzzoBTR5CSuruD8yuxQ8nbgvSBSuEXDEtX06vOREoI40rhVFiMfTn2wz_K2oDtFSiaUsntkuD9TIIEpno7RsiNwuRdxzrdAghOkUtq9HhIWFThvFnGQ',

        'Cookie': 'cookie01=2.1c.61.cab82412.50; Hm_lvt_5288aab03e95c23535085e433fce1276=1595659269,1595659459,1595659541,1595661398; code=mH7D7O5vAFI%3D; c=zkNnQVmuXng%3D; Hm_lpvt_5288aab03e95c23535085e433fce1276=1595688865; xx=CfDJ8Fm7NrMhvXlOvG3aU2QSK8dUP_qMI51dbFKcfVU1GXqKaTSJHwGqXkAq8CGTWxbPPZzsSVuVmibT-fu_Do-mVA_F8oJnv-ghk9M2HEHTRpNGXBXnXBMoWl4vu7_d8V-JTKKvpsiJV0MGFbtaMMttWxVG1YrvXo_-RDdSS1NUqBawe-0dSEQAc_jYeMdPZsuPviX5fWNaITEoK60SeuLH9jWirXsY0EtQKw68xKEBYr63VL4CvvhyEAkxG4EIT-C92CcYvcdX16Nl8L03ViEld4p9fGrZJvVKoK9ri1jWUj1uNVBlru7syj2Q9EnJfuiVNvX5nnPDtdrJeW70Ii6HQtEpXaRfzeWowTyhBDuqWaRKid23vP7QwbxFHiiXHE0Bu6ceUkC9jKAbMUIZYgNQRG3G5yAsHEGwCekbMvoG1t8maSq5st-Ahou_SpiAvWL8oJFvA2C-DlX180xyZG2tOP0hjemYl2rakMX5PNwVScWC5pP_caa_sNbd72BGyEBADQ',

        'Cookie': 'cookie01=2.1c.61.cab82412.50; Hm_lvt_5288aab03e95c23535085e433fce1276=1595659269,1595659459,1595659541,1595661398; code=mH7D7O5vAFI%3D; c=6LB5%2BQKA%2FVQ%3D; xx=CfDJ8Fm7NrMhvXlOvG3aU2QSK8dcFeLdP8mjho2k2bMZIjQpGMbxbyJSsLqwzEzPMMJVBSIkG3w_U3Ig_VfqE4t3ehKTaTrNs1N1uCiywKVGkB4HQc_PWQRsGKY7N9MEP2KllDNeyI0lVPI7aZdsKiLRx14i4Xhu_dUXy7JcumXF2u9CoCTj_3hherU5NXej244IjRfSe8PLw4mSPI3J8yju6i5VBqLfZGjUZrVQZrkieMQYZDWkXwY2w4cLhmJMtWrOx7P-YB6LY0o7w4T_ZoWXKoEm6_oKQisSgdCWfXU7uqbnL-0YFgIzQs56MA5ZnAjCqSojnIy5s518WPc4kAYosULAyF7RA5CqP-0Jgf3KRqNgs2BY5nP41xLWZlxJsDfNvFbjnTK7LZ8fFJ1scni1voq1aNLjqZIubGyBf3S-QiR7jqTMuNVcDOfID1IctYZgR-QD_kIUVYnfrRYPGnh2v3pRRg45kykyVi-z17CVzjy2A0cKyLvqzDJVnLWIdwQ9LA; Hm_lpvt_5288aab03e95c23535085e433fce1276=1595699891',

        'Cookie': 'cookie01=2.1c.61.cab82412.50; Hm_lvt_5288aab03e95c23535085e433fce1276=1595659269,1595659459,1595659541,1595661398; code=mH7D7O5vAFI%3D; c=6LB5%2BQKA%2FVQ%3D; Hm_lpvt_5288aab03e95c23535085e433fce1276=1595702743; xx=CfDJ8Fm7NrMhvXlOvG3aU2QSK8cg0SAxLhIPSV_Y2XMSgiBqOozrTsK0wrXgKVS6Yg_kYKvGw7-Q8H3H8oPdnUvb_Xs2CtnmTs9GdB3phd8r3JYVZ_juJnbp5Ye1aLziqao09z9qg5P6RW13Xp7cvcpTJq9Yg92PbPRbRW565gSqa8Pd2zs_UCNw8EBEAHvbxpY-7j4ddFntx9VXHKgkAgdu52XCrUxZOpk52-Hsp8SvpDAslT56Ob1aNVV0JUmMsv1X5uIfcOIVKHxpr0TayiKU5I9OTa1v06uDLD6sqOmTfk8F4stu9jQvovsqh04SNM8yxFmp07L3pkzXTjea9y--f4E0CHtstA3A2HLTGuam9JUDOHk9NplOn2KX6ZhFu5ptf9hLd0hKsOosoICB7ldP5-oaqx3RLNGxo3DGOLsCS1u-MnCynwwMLkz-SGiA6zgfHYQ7gPnGoIpECHSaLG5E9FGNr3epBkdbY9osX8JZ5RjXV1hUl22RheR4GEyaTiSTgQ',
    }

    # ips = []
    # path = './ip_.txt'
    # ip_list =  read(path)
    # for i in ip_list:
    #     print(i, checkip(i))
    #     if checkip(i):
    #         ips.append(i)
    # print(ips)
    ips2 = [
        '218.241.219.84:3128',
        '221.180.170.104:8080',
        '115.223.2.114:80',
        '122.51.49.88:8888',
        '103.103.0.140:80',
        '218.60.8.99:3129',
        '122.51.49.88:8888',
        '116.196.85.150:3128',
        '119.84.112.139:80',
        '218.60.8.99:3129',
        '221.122.91.64:80',
        '116.196.85.150:3128',
    ]
    ips3 = ['218.241.219.84:3128', '115.223.2.114:80', '103.103.0.140:80', '218.60.8.99:3129', '116.196.85.150:3128',
            '119.84.112.139:80', '218.60.8.99:3129', '221.122.91.64:80', '116.196.85.150:3128']

    reg(url, random.choice(ips3), flag=False)

    # threads = [threading.Thread(target=reg, args=(url, ip)) for ip in ips3]
    # for t in threads:
    #     t.start()
    # for t in threads:
    #     t.join()
