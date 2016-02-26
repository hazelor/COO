__author__ = 'sonic-server'

from base import base_handler
import tornado.web
import tornado.ioloop
import time

class ctrl_handler(base_handler):
    @tornado.web.asynchronous
    def get(self):
        tornado.ioloop.IOLoop.instance().add_timeout(time.time()+10, self.on_end)
    def on_end(self):
        if self.request.connection.stream.closed():
            return
        self.write('UserChannel')
        self.finish()
