__author__ = 'guoxiao'

from base import base_handler
import tornado
import json
import tcelery
import tasks_for_syn
# from util.confs import g_chamber_conf
from util.dbtool import *
import time

class preview_handler(base_handler):
    @tornado.web.authenticated
    def get(self):
        mac_address_list = (self.current_user).strip().split(',')
        g_chamber_conf=[]
        for item in mac_address_list:
            sql = "select mac_address_position,name from air_chamber where mac_address='%s' " % (item)
            with database_resource() as cursor:
                cursor.execute(sql)
                data = cursor.fetchall()
            if data:
                g_chamber_conf += data
        current_key = self.get_argument('current_key','')
        if current_key == '':
            current_key = g_chamber_conf[0]
        return self.render('preview.html',
                           page_name = 'preview',
                           current_key = current_key,
                           chambers = g_chamber_conf,
                           )
    def on_connection_close(self):
        print 'preview on_connection_close method called'

# tcelery.setup_nonblocking_producer()

class preview_realtime_handler(base_handler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        current_chamber_key = self.get_argument('current_chamber_key', '')
        if current_chamber_key != '':
            mac_address = current_chamber_key.split(',')[0]
            position = current_chamber_key.split(',')[1]
            # tasks.redis_query.apply_async(args=[mac_address, postion], callback=self.on_success)
            # response = yield tornado.gen.Task(tasks.redis_query, args=[mac_address, postion])
            response = yield tasks_for_syn.redis_query(mac_address, position)
            self.on_success(response)
            # yield tornado.gen.Task(tornado.ioloop.IOLoop.instance().add_timeout, time.time() + 1)
            # self.write('')
            # self.finish()
    def on_success(self, resp):
        data=[]
        if len(resp[0]) != 0:
            data.append(resp[0])
        else:
            data.append('')
        try:
            plot_data = resp[1]
            for i in xrange(0,len(resp[1])):
                if plot_data[i][0] and plot_data[i][1]:
                    plot_data[i][0]=float(plot_data[i][0])*1000
                    plot_data[i][1]=float(plot_data[i][1])
                else:
                    plot_data[i][0]=''
                    plot_data[i][1]=''
                # if plot_data[1][0] and plot_data[1][1]:
                    # plot_data[1][0]=float(plot_data[1][0])*1000
                    # plot_data[1][1]=float(plot_data[1][1])
                # else:
                    # plot_data[1][0]=''
                    # plot_data[1][1]=''
            data.append(plot_data)
        except:
            data.append('')
        data=json.dumps(data)
        self.write(data)
        self.finish()
    # def on_success(self, resp):
    #     data=[]
    #     if len(resp.result[0]) != 0:
    #         data.append(resp.result[0])
    #     else:
    #         data.append('')
    #     try:
    #         plot_data = resp.result[1]
    #         if plot_data[0][0] and plot_data[0][1]:
    #             plot_data[0][0]=float(plot_data[0][0])*1000
    #             plot_data[0][1]=float(plot_data[0][1])
    #         else:
    #             plot_data[0][0]=''
    #             plot_data[0][1]=''
    #         if plot_data[1][0] and plot_data[1][1]:
    #             plot_data[1][0]=float(plot_data[1][0])*1000
    #             plot_data[1][1]=float(plot_data[1][1])
    #         else:
    #             plot_data[1][0]=''
    #             plot_data[1][1]=''
    #         # plot_data[1][0]=float(plot_data[1][0])*1000
    #         # plot_data[1][1]=float(plot_data[1][1])
    #         data.append(plot_data)
    #     except:
    #         data.append('')
    #     data=json.dumps(data)
    #     self.write(data)
    #     self.finish()
    def on_connection_close(self):
        print 'preview_realtime on_connection_close method called'

