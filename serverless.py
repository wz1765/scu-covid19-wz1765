# -*- coding: utf8 -*-
"""
author: Les1ie, HyperMn
mail: me@les1ie.com
license: CC BY-NC-SA 3.0
"""

import pytz
import requests
from datetime import datetime


s = requests.Session()

user = "USERNAME"    # 账号
passwd = "PASSWORD"   # 密码
api_key = ""  # server酱的api，填了可以微信通知打卡结果，不填没影响


def login(s: requests.Session, username, password):
    # r = s.get(
    #     "https://app.ucas.ac.cn/uc/wap/login?redirect=https%3A%2F%2Fapp.ucas.ac.cn%2Fsite%2FapplicationSquare%2Findex%3Fsid%3D2")
    # print(r.text)
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
        'realname': old['realname'],    #姓名
        'number': old['number'],        #学工号
        'sfzx': old['sfzx'],            #是否在校
        'ismoved': old['ismoved'],      #？所在地点
        'tw': old['tw'],                #体温
        'sftjwh': old['sftjwh'],        #是否途经武汉
        'sftjhb': old['sftjhb'],        #是否途经湖北
        'sfcxtz': old['sfcxtz'],        #是否出现体征？
        'sfjcwhry': old['sfjcwhry'],    #是否接触武汉人员
        'sfjchbry': old['sfjchbry'],    #是否接触湖北人员
        'sfjcbh': old['sfjcbh'],        #是否接触病患 ？疑似/确诊人群
        'sfcyglq': old['sfcyglq'],      #是否处于隔离期？
        "sfjxhsjc": old['sfjxhsjc'],    #是否进行核酸检查
        'sfcxzysx': old['sfcxzysx'],    #是否出现值得注意的情况？
        'szsqsfybl': old['szsqsfybl'],
        'sfsqhzjkk': old['sfsqhzjkk'],
        'sfygtjzzfj': old['sfygtjzzfj'],
        'hsjcjg': old['hsjcjg'],
        'old_szdd': old['old_szdd'],        #所在地点
        'sfsfbh': old['sfsfbh'],            #是否？？病患
        'geo_api_info': old['old_city'],
        'old_city': old['old_city'],
        'geo_api_infot': old['geo_api_infot'],
        'date': datetime.now(tz=pytz.timezone("Asia/Shanghai")).strftime("%Y-%m-%d"),
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

def main_handler(event, context):
    """
    腾讯云云函数入口
    """
    print(datetime.now(tz=pytz.timezone("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S %Z"))
    login(s, user, passwd)
    yesterday = get_daily(s)
    submit(s, yesterday)

