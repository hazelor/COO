__author__ = 'guoxiao'

from base import base_handler
import tornado
import json
import tcelery
import tasks
from util.confs import g_chamber_conf

class preview_handler(base_handler):
    def get(self, *args, **kwargs):
        current_key = self.get_argument('current_key','')
        if current_key == '':
            current_key = g_chamber_conf.keys()[0]
        return self.render('preview.html',
                           page_name = 'preview',
                           current_key = current_key,
                           chambers = g_chamber_conf,
                           )

tcelery.setup_nonblocking_producer()

class preview_realtime_handler(base_handler):
    @tornado.web.asynchronous
    def get(self):
        current_chamber_key = self.get_argument('current_chamber_key', '')
        if current_chamber_key != '':
            # print current_chamber_key
            mac_address = current_chamber_key.split(',')[0]
            postion = current_chamber_key.split(',')[1]
            # type = 'measured_concentration'
            # print mac_address
            # print postion
            tasks.redis_query.apply_async(args=[mac_address, postion], callback=self.on_success)
    def on_success(self, resp):
        data=[]
        if len(resp.result[0]) != 0:
            data.append(resp.result[0])
        else:
            data.append('')
        try:
            plot_data = resp.result[1]
            plot_data[0][0]=float(plot_data[0][0])*1000
            plot_data[0][1]=float(plot_data[0][1])
            plot_data[1][0]=float(plot_data[1][0])*1000
            plot_data[1][1]=float(plot_data[1][1])
            data.append(plot_data)
        except:
            data.append('')
        # print data
        data=json.dumps(data)
        self.write(data)
        self.finish()

