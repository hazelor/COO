__author__ = 'sonic-server'

# import tornado
import tornado.web

class base_handler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        return