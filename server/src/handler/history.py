#!/usr/bin/python
#-*-coding:utf-8-*-

__author__ = 'guoxiao'

from base import base_handler
import tornado
import tcelery
import tasks
from util.confs import *
import json
from util.commons import *
import time
from util.dbtool import *
import time



class history_handler(base_handler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        current_chamber_key = self.get_argument('current_chamber_key','')
        mac_address_list = (self.current_user).strip().split(',')
        g_chamber_conf=[]
        for item in mac_address_list:
            sql = "select mac_address_position,name,member from air_chamber where mac_address='%s' " % (item)
            with database_resource() as cursor:
                cursor.execute(sql)
                data = cursor.fetchall()
            if data:
                g_chamber_conf += data
        # print current_chamber_key
        if current_chamber_key == '':
            current_chamber_key = g_chamber_conf[0]
            current_member_list = g_chamber_conf[0][2].strip().split('_')
            data_list=[]
            for item in current_member_list:
                data_list.append((short_name_to_english_name[item], short_name_to_chinese_name[item]))
            # current_data_key = g_chamber_conf[current_chamber_key]['data_contents'].keys()[0]
            return self.render('history.html',
                                page_name = 'history',
                                current_chamber_key = current_chamber_key,
                                current_data_key = data_list[0][0],
                                chamber_dict = g_chamber_conf,
                                data_list = data_list)
        else:
            #for ajax to update the data_content
            # print current_chamber_key
            sql = "select member from air_chamber where mac_address_position='%s' " % (current_chamber_key)
            with database_resource() as cursor:
                cursor.execute(sql)
                data = cursor.fetchone()
            if data:
                data_list=[]
                current_member_list = data[0].strip().split('_')
                for item in current_member_list:
                    data_list.append((short_name_to_english_name[item], short_name_to_chinese_name[item]))
            j_data_contents = json.dumps(data_list)
            self.write(j_data_contents)



tcelery.setup_nonblocking_producer()

class history_query_handler(base_handler):
    @tornado.web.asynchronous
    def get(self):
        # time.sleep(10)
        mac_address=self.get_argument('mac_address')
        # mac_address=get_md5(mac_address)
        position=self.get_argument('position')
        type=self.get_argument('type')
        # print type[2:-2]
        start_time=self.get_argument('start_time')+':00'
        start_time = time.mktime(time.strptime(start_time, '%Y-%m-%d %H:%M:%S'))
        end_time=self.get_argument('end_time')+':00'
        end_time = time.mktime(time.strptime(end_time, '%Y-%m-%d %H:%M:%S'))
        # print start_time
        # print end_time
        if type == '':
            tasks.db_query.apply_async(args=[mac_address, position, type, start_time, end_time], callback=self.on_success_all)
        else:
            tasks.db_query.apply_async(args=[mac_address, position, type, start_time, end_time], callback=self.on_success_one)
    def on_success_one(self, resp):
        #print resp.result
        res = []
        if resp.result:
            # print resp.result
            for d,v in resp.result:
                res.append([d*1000,v])
            # print res
            self.write(json.dumps(res))
        else:
            # print 'here'
            self.write('')
        self.finish()

    def on_success_all(self, resp):
        res=[[],[]]
        if resp.result:
            for d,v in resp.result[0]:
                res[0].append([d*1000,v])
            for d,v in resp.result[1]:
                res[1].append([d*1000,v])
            self.write(json.dumps(res))
        else:
            self.write('')
        self.finish()
