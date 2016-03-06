__author__ = 'sonic-server'

from base import base_handler
import tornado.web
import tornado.ioloop
# import time
import tcelery
import tasks
import json


tcelery.setup_nonblocking_producer()

class ctrl_handler(base_handler):
    @tornado.web.asynchronous
    def post(self):
        jdata = json.loads(self.request.body)
        mac_address = jdata['mac_address']
        sql="select duration from device WHERE mac_address='%s' "%(mac_address)
        tasks.db_query_basic.apply_async(args=[sql], callback=self.on_success)
    def on_success(self, resp):
        resp = json.dumps(resp.result)
        # print resp
        self.write(resp[0][0])
        self.finish()
