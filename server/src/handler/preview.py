__author__ = 'guoxiao'

from base import base_handler
import tornado
import json
import tcelery
import tasks

class preview_handler(base_handler):
    def get(self, *args, **kwargs):
        chambers = []
        return self.render('preview.html',
                           page_name = 'preview',
                           chambers = chambers,
                           )

tcelery.setup_nonblocking_producer()

class preview_realtime_handler(base_handler):
    @tornado.web.asynchronous
    def get(self):
        mac_address = self.get_argument('mac_address')
        postion = self.get_argument('postion')
        type = self.get_argument('type')
        tasks.redis_query.apply_async(args=[mac_address, postion, type], callback=self.on_success)
    def on_success(self, resp):
        self.write(resp.result)
        self.finish()

