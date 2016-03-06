__author__ = 'sonic-server'

# import tornado
import tornado.web

class base_handler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie('username')