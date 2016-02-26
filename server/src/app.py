__author__ = 'sonic-server'

import os
import tornado.web
import tornado.ioloop
import tornado.options
from tornado.options import define,options
import tcelery


import routes

define('port', default=8080, type=int)
define('debug', default=True, type=bool)

# options.logging = 'debug' if options.debug else 'info'
options.logging = 'info'

def create_app():
    settings = {
        'static_path':'static',
        'template_path':'template',
        'xsrf_cookies':False,
        'debug':options.debug,
        'ui_modules':routes.modules,
    }
    return tornado.web.Application(routes.handlers, **settings)

if __name__ == '__main__':
    # tcelery.setup_nonblocking_producer()
    tornado.options.parse_command_line()
    app = create_app()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
