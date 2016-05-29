__author__ = 'sonic-server'

from base import base_handler
import tornado.web
import tornado.ioloop
import time
import tcelery
import tasks_for_syn
import json
import tornado.gen
import gc

# tcelery.setup_nonblocking_producer()

class ctrl_handler(base_handler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        jdata = json.loads(self.request.body)
        print "ctrl:",jdata
        mac_address = jdata['mac_address']
        sql="select duration from device WHERE mac_address='%s' "%(mac_address)
        # response = yield tornado.gen.Task(tasks.db_query_basic.apply_async, args=[sql])
        # response = yield tornado.gen.Task(tasks.db_query_basic, args=[sql])
        response = yield tasks_for_syn.db_query_basic(sql)
        # if response.result:
        #     data = response.result[0][0]
        #     self.write(data)
        if response:
            data = response[0][0]
            data = str(int(data)-1)
            self.write(data)
        self.finish()
        # tornado.ioloop.IOLoop.instance().add_callback(self.finish)
    # @tornado.web.asynchronous
    # @tornado.gen.coroutine
    def on_success(self, resp):
        # if resp == '':
        #     self.write(resp)
        # yield tornado.gen.Task(tornado.ioloop.IOLoop.instance().add_timeout,time.time()+200)
        if resp.result:
            data = resp.result[0][0]
            self.write(data)
        # tornado.ioloop.IOLoop.instance().add_callback(self.finish())
        self.finish()
    # def on_finish(self):
        # print 'on_finish method called'
    def on_connection_close(self):
        print 'ctrl on_connection_close method called'
