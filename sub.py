'''
！！！必看！！！
进入https://wfw.scu.edu.cn/ncov/wap/default/index即打卡网页，登录后在“所在地点”中获取当前位置信息，
然后F12，在element里面用ctrl+f搜索geo_api_info，把对应位置的geo_api_info的内容复制到https://www.sojson.com/yasuo.html
先"去除转义"再"unicode转中文"，把获取的结果复制到下面对应的geo_api_info的位置，此脚本中地址默认为四川大学江安校区。
'''

# -*- coding: utf-8 -*-
"""
Modified on 20200917
@author: HyperMn
"""

"""
author: Les1ie
mail: me@les1ie.com
license: CC BY-NC-SA 3.0
"""

import pytz
import requests
from time import sleep,time
from random import randint
from datetime import datetime


s = requests.Session()
header = {"User-Agent": "Mozilla/5.0 (Linux; Android 10;  AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045136 Mobile Safari/537.36 wxwork/3.0.16 MicroMessenger/7.0.1 NetType/WIFI Language/zh",}
s.headers.update(header)

user = "2017141443041"    # 账号
passwd = "040030"   # 川大统一认证密码
api_key = "你的server酱api"  # server酱的api，填了可以微信通知打卡结果，不填没影响

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
    # info = s.get("https://app.ucas.ac.cn/ncov/api/default/index?xgh=0&app_id=ucas")
    j = daily.json()
    d = j.get('d', None)
    if d:

        return daily.json()['d']
    else:
        print("获取昨日信息失败")
        exit(1)


def submit(s: requests.Session, old: dict):
    new_daily = {
        "qksm": old["qksm"],
        "remark": old["remark"],
        "gllx": old["gllx"],
        "glksrq": old["glksrq"],
        "jcbhlx": old["jcbhlx"],
        "jcbhrq": old["jcbhrq"],
        "bztcyy": old["bztcyy"],
        "szcs": old["szcs"],
        "szgj": old["szgj"],
        "jcjg": old["jcjg"],
        "jcqzrq": old["jcqzrq"],
        "sfjcqz": old["sfjcqz"],
        "sfjxhsjc": old['sfjxhsjc'],    #是否进行核酸检查 1
        'hsjcjg': old['hsjcjg'],        #核算检测结果 2
        "hsjcrq": "2020-09-11",
        "hsjcdd": "四川大学华西医院",
        "szxqmc": "江安校区",
        'tw': old['tw'],                #体温 3
        'sfcxtz': old['sfcxtz'],        #是否出现体征？ 4
        'sfjcbh': old['sfjcbh'],        #是否接触病患 ？疑似/确诊人群 5
        'sfcxzysx': old['sfcxzysx'],    #是否出现值得注意的情况？ 6
        'sfyyjc': old['sfyyjc'], #是否医院检查？ 7
        'jcjgqr': old['jcjgqr'], #检查结果确认？ 8
        'address': old['address'], # 9
        'geo_api_info': '{"type":"complete","position":{"Q":30.629940049914,"R":104.0849476454,"lng":104.084948,"lat":30.62994},"location_type":"html5","message":"Get sdkLocation failed.Get geolocation success.Convert Success.Get address success.","accuracy":40,"isConverted":true,"status":1,"addressComponent":{"citycode":"028","adcode":"510107","businessAreas":[{"name":"小天竺","id":"510107","location":{"Q":30.639354,"R":104.06894199999999,"lng":104.068942,"lat":30.639354}},{"name":"跳伞塔","id":"510107","location":{"Q":30.636149,"R":104.07122400000003,"lng":104.071224,"lat":30.636149}}],"neighborhoodType":"科教文化服务;学校;高等院校","neighborhood":"四川大学","building":"","buildingType":"","street":"科华北路","streetNumber":"131号","country":"中国","province":"四川省","city":"成都市","district":"武侯区","township":"望江路街道"},"formattedAddress":"四川省成都市武侯区望江路街道四川大学四川大学望江校区","roads":[],"crosses":[],"pois":[],"info":"SUCCESS"}', # 10
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
	    'zgfxdq': old['zgfxdq'],
	    'mjry': old['mjry'],
	    'csmjry': old['csmjry'],
        "created_uid": old["created_uid"]
        }

    r = s.post("https://wfw.scu.edu.cn/ncov/wap/default/save", data=new_daily)
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
    for i in range(randint(10,600),0,-1):
        print("\r等待{}秒后填报".format(i),end='')
        sleep(1)

    login(s, user, passwd)
    yesterday = get_daily(s)
    submit(s, yesterday)
