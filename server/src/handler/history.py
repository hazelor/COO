__author__ = 'guoxiao'

from base import base_handler
import tornado
import tcelery
import tasks
from util.confs import g_chamber_conf
import json



class history_handler(base_handler):
    def get(self, *args, **kwargs):
        current_chamber_key = self.get_argument('current_chamber_key','')
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
            j_data_contents = json.dumps(g_chamber_conf[current_chamber_key])
            self.write(j_data_contents)



tcelery.setup_nonblocking_producer()

class history_query_handler(base_handler):
    @tornado.web.asynchronous
    def get(self):
        mac_address=self.get_argument('mac_address')
        postion=self.get_argument('postion')
        type=self.get_argument('type')
        start_time=self.get_argument('start_time')
        end_time=self.get_argument('end_time')
        tasks.db_query.apply_async(args=[mac_address, postion, type, start_time, end_time], callback=self.on_success)
    def on_success(self, resp):
        self.write(resp.result)
        self.finish()
