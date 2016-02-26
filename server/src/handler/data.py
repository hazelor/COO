from .base import base_handler
import tornado
import json
import tcelery
import tasks


tcelery.setup_nonblocking_producer()

class data_handler(base_handler):
    @tornado.web.asynchronous
    def post(self):
        jdatas = json.loads(self.request.body)
        tasks.db_save.apply_async(args=[jdatas], callback=self.on_success)
    def on_success(self, resp):
        self.write(resp.result)
        self.finish()
