#!/bin/env python
# coding:utf8


import sys
import requests
import json
import pickle
import time
import datetime


#reload(sys)
#sys.setdefaultencoding('utf-8')

WECHAT_CORPID = CORPID
WECHAT_SECRET = SECRET
API_URL = 'https://qyapi.weixin.qq.com/cgi-bin/'
TOKEN_URL = API_URL+'gettoken?corpid={id}&corpsecret={secrect}'


def save_token(file_name):
    end_time = datetime.datetime.now() + datetime.timedelta(hours=2)
    end_time_ts = time.mktime(end_time.timetuple())
    url = TOKEN_URL.format(id=WECHAT_CORPID, secrect=WECHAT_SECRET)
    resp = requests.get(url)
    wechat_token = resp.json()['access_token']
    token = {'token':wechat_token, 'valid_end_time': end_time_ts}
#    with open(file_name,'wb') as f:
#        pickle.dump(token,f)
    return wechat_token


def get_token(file_name):
    try:
        with open(file_name) as f:
            token = pickle.load(f)
    except Exception as e:
        token = save_token(file_name)
    if token['valid_end_time'] <= time.time():
        token = save_token(file_name) 
    return token['token']


def send_message(message, token):
    url = API_URL+'message/send?access_token={token}'
    msg_data = {
        'touser': '@all',
        'msgtype': 'text',
        'agentid': 1,
        'text': {'content': message}
    }
    resp = requests.post(url.format(token=token), data=json.dumps(msg_data))


def main():
    try:
        message = sys.argv[2] + '\n' + sys.argv[3]
    except Exception as e:
        message = "Nothing is get from zabbix,So,this is default message for debug"
    token = save_token('token.info')
    send_message(message, token)


main()


