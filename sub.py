# -*- coding: utf-8 -*-
"""
Modified on Mon Apr 20 21:31:53 2020

@author: Les1ie, HyperMn
mail: me@les1ie.com, hypermn@163.com
license: CC BY-NC-SA 3.0
"""

import pytz
import requests
from time import sleep
from random import randint
from datetime import datetime

'''
！！！必看！！！
进入https://wfw.scu.edu.cn/ncov/wap/default/index即打卡网页，登录后在“所在地点”中获取当前位置信息，
然后F12，在element里面用ctrl+f搜索geo_api_info，把对应位置的geo_api_info的内容复制到https://www.sojson.com/yasuo.html
先"去除转义"再"unicode转中文"，把获取的结果复制到下面的my_geo_info的位置。
'''

my_geo_info = '请阅读上方文字，覆盖此处'
s = requests.Session()
header = {"User-Agent": "Mozilla/5.0 (Linux; Android 10;  AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045136 Mobile Safari/537.36 wxwork/3.0.16 MicroMessenger/7.0.1 NetType/WIFI Language/zh",}
s.headers.update(header)

user = "USERNAME"    # 账号, 13位学号
passwd = "PASSWORD"   # 密码， SCU统一认证登录密码
api_key = "API_KEY"  # server酱的api，填了可以微信通知打卡结果，不填没影响


def login(s: requests.Session, username, password):
    #r = s.get(
    #    "https://app.ucas.ac.cn/uc/wap/login?redirect=https%3A%2F%2Fapp.ucas.ac.cn%2Fsite%2FapplicationSquare%2Findex%3Fsid%3D2")
    #print(r.text)
    payload = {
        "username": username,
        "password": password
    }
    r = s.post("https://wfw.scu.edu.cn/a_scu/api/sso/check", data=payload)

    # print(r.text)
    if r.json().get('m') != "操作成功":
        print(r.text)
        print("登录失败")
        exit(1)


def get_daily(s: requests.Session):
    daily = s.get("https://wfw.scu.edu.cn/ncov/api/default/daily?xgh=0&app_id=scu")
    j = daily.json()
    d = j.get('d', None)
    if d:

        return daily.json()['d']
    else:
        print("获取昨日信息失败")
        exit(1)


def submit(s: requests.Session, old: dict):
    new_daily = {
        "sfjxhsjc": old['sfjxhsjc'],    #是否进行核酸检查 1
        'hsjcjg': old['hsjcjg'],        #核算检测结果 2
        'tw': old['tw'],                #体温 3
        'sfcxtz': old['sfcxtz'],        #是否出现体征？ 4
        'sfjcbh': old['sfjcbh'],        #是否接触病患 ？疑似/确诊人群 5
        'sfcxzysx': old['sfcxzysx'],    #是否出现值得注意的情况？ 6
        'sfyyjc': old['sfyyjc'], #是否医院检查？ 7
        'jcjgqr': old['jcjgqr'], #检查结果确认？ 8
        'address': old['address'], # 9
        'geo_api_info': my_geo_info, # 注意，此处my_geo_info需要手动更改
        'area': old['area'], # 11
        'province': old['province'], # 12
        'city': old['city'], # 13
        'sfzx': old['sfzx'],            #是否在校 14
        'sfjcwhry': old['sfjcwhry'],    #是否接触武汉人员 15 
        'sfjchbry': old['sfjchbry'],    #是否接触湖北人员 16
        'sfcyglq': old['sfcyglq'],      #是否处于隔离期？ 17
        'sftjhb': old['sftjhb'],        #是否途经湖北 18
        'sftjwh': old['sftjwh'],        #是否途经武汉 19
        'date': datetime.now(tz=pytz.timezone("Asia/Shanghai")).strftime("%Y%m%d"), # 20
        'uid': old['uid'],
        'created': str(int(time())),  # 创建时间
        'szsqsfybl': old['szsqsfybl'],  # 21
        'sfsqhzjkk': old['sfsqhzjkk'],  # 22
        'sfygtjzzfj': old['sfygtjzzfj'],# 23 
        'ismoved': old['ismoved'],      #？所在地点 24
        'old_szdd': old['old_szdd'],        #所在地点
        'sfsfbh': old['sfsfbh'],            #是否？？病患
    	'szsqsfybl': old['szsqsfybl'],
    	'sfsqhzjkk': old['szsqsfybl'],
	'sfygtjzzfj': old['szsqsfybl'],
	'zgfxdq': old['zgfxdq'],
	'mjry': old['mjry'],
	'csmjry': old['csmjry'],
        'old_city': old['old_city'],
        'is_daily': old['is_daily'],
        'realname': old['realname'],    #姓名
        'number': old['number'],        #学工号
        'app_id': 'scu'}


    r = s.post("https://wfw.scu.edu.cn/ncov/api/default/save", data=new_daily)
    print("提交信息:", new_daily)
    # print(r.text)
    result = r.json()
    if result.get('m') == "操作成功":
        print("打卡成功")
        if api_key:
            message(api_key, result.get('m'), new_daily)
    else:
        print("打卡失败，错误信息: ", r.json().get("m"))
        if api_key:
            message(api_key, result.get('m'), new_daily)


def message(key, title, body):
    """
    微信通知打卡结果
    """
    msg_url = "https://sc.ftqq.com/{}.send?text={}&desp={}".format(key, title, body)
    requests.get(msg_url)


if __name__ == "__main__":
    print(datetime.now(tz=pytz.timezone("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S %Z"))
    
    #手动执行可注释以下三行的延迟填报
    for i in range(randint(10,600),0,-1):
        print("\r等待{}秒后填报".format(i),end='')
        sleep(1)

    login(s, user, passwd)
    yesterday = get_daily(s)
    submit(s, yesterday)
