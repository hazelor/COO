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
    def get(self):
        jdata = json.loads(self.request.body)
        mac_address = jdata['mac_address']
        tasks.interval_redis_query.apply_async(args=[mac_address], callback=self.on_success)
        # tornado.ioloop.IOLoop.instance().add_timeout(time.time()+10, self.on_end)
    def on_success(self, resp):
        # if self.request.connection.stream.closed():
        #     return
        self.write(resp.result)
        self.finish()
