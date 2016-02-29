__author__ = 'guoxiao'

from base import base_handler
import tornado
import tcelery
import tasks
from util.confs import g_chamber_conf
import json
from util.commons import *
import time



class history_handler(base_handler):
    def get(self, *args, **kwargs):
        current_chamber_key = self.get_argument('current_chamber_key','')
        # print current_chamber_key
        if current_chamber_key == '':
            current_chamber_key = g_chamber_conf.keys()[0]
            current_data_key = g_chamber_conf[current_chamber_key]['data_contents'].keys()[0]
            return self.render('history.html',
                                page_name = 'history',
                                current_chamber_key = current_chamber_key,
                                current_data_key = current_data_key,
                                chamber_dict = g_chamber_conf,
                                data_dict = g_chamber_conf[current_chamber_key]['data_contents'])
        else:
            #for ajax to update the data_content
            j_data_contents = json.dumps(g_chamber_conf[current_chamber_key]['data_contents'])
            self.write(j_data_contents)



tcelery.setup_nonblocking_producer()

class history_query_handler(base_handler):
    @tornado.web.asynchronous
    def get(self):
        mac_address=self.get_argument('mac_address')
        mac_address=get_md5(mac_address)
        position=self.get_argument('position')
        type=self.get_argument('type')
        # print type
        start_time=self.get_argument('start_time')+':00'
        start_time = time.mktime(time.strptime(start_time, '%Y-%m-%d %H:%M:%S'))
        end_time=self.get_argument('end_time')+':00'
        end_time = time.mktime(time.strptime(end_time, '%Y-%m-%d %H:%M:%S'))
        # print start_time
        # print end_time
        tasks.db_query.apply_async(args=[mac_address, position, type, start_time, end_time], callback=self.on_success)
    def on_success(self, resp):
        #print resp.result
        res = []
        if resp.result:
            for d,v in resp.result:
                res.append([d*1000,v])
            print res
            self.write(json.dumps(res))
        else:
            self.write('')
        self.finish()
