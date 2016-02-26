#!/usr/bin/env python
#--coding:utf-8--

__author__ = 'guoxiao'

import time,os
import json
import urllib2
import urllib
from commUtils import *
from queueUtils import DataPool
from macros import *
from confUtils import set_update_duration, get_update_duration


def update_data(c_data):
    url = "http://{0}:{1}{2}".format(SERVER_URL, UPDATE_PORT, API_DATACHANNEL_URL)
    j_data = json.dumps(c_data)
    req = urllib2.Request(url, j_data)
    try:
        res = urllib2.urlopen(req)
        if res.read().strip() == RES_SUCCESS:
            return True
        else:
            return False
    except Exception as e:
        return False


def update_ctrl():
    url = "http://{0}:{1}{2}".format(SERVER_URL, UPDATE_PORT, API_CTRL_URL)
    try:
        res = urllib2.urlopen(url)
        j_res = json.loads(res.read())
        duration = int(j_res['duration'])
        if duration == get_update_duration():
            return
        set_update_duration(duration)
        CountDownExec.get_instance('serial_update').set_duration(duration)
        CountDownExec.get_instance('net_update').set_duration(duration)
    except Exception as e:
        return


def exe_update(args):
    dp = DataPool.get_instance()
    length = dp.get_len() if dp.get_len()<10 else 10
    #print length

    c_datas = []
    for i in range(length):
        res = dp.pull_data()
        if res:
            c_datas.append(res)
    if c_datas:
        res = update_data(c_datas)
        print res
        if not res:
            for cd in c_datas:
                dp.push_data(cd)

def exe_ctrl(args):
    update_ctrl()
