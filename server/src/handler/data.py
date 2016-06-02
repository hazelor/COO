from .base import base_handler
import tornado
import json
import tcelery
import tasks_for_syn
import time
import gc

# tcelery.setup_nonblocking_producer()

class data_handler(base_handler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        jdatas = json.loads(self.request.body)
        print "updata:",jdatas
        # response = yield tornado.gen.Task(tasks.db_save, args=[jdatas])
        response = yield tasks_for_syn.db_save(jdatas)
        # self.write(response.result)
        self.write(response)
        # tornado.ioloop.IOLoop.instance().add_callback(self.finish)
        self.finish()
        # tasks.db_save.apply_async(args=[jdatas], callback=self.on_success)
    # @tornado.web.asynchronous
    # @tornado.gen.coroutine
    def on_success(self, resp):
        # yield tornado.gen.Task(tornado.ioloop.IOLoop.instance().add_timeout, time.time()+200)
        self.write(resp.result)
        self.finish()
    def on_connection_close(self):
        print 'data on_connection_close method called'
