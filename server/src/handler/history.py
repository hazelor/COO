__author__ = 'guoxiao'

from base import base_handler
import tornado
import tcelery
import tasks


class history_handler(base_handler):
    def get(self, *args, **kwargs):
        return self.render('history.html',
                           page_name = 'history',
                           )

tcelery.setup_nonblocking_producer()

class history_query_handler(base_handler):
    @tornado.web.asynchronous
    def get(self):
        mac_address=self.get_argument('mac_address')
        postion=self.get_argument('postion')
        type=self.get_argument('type')
        start_time=self.get_argument('start_time')
        end_time=self.get_argument('end_time')
        tasks.db_query.apply_async(args=[mac_address, postion, type, start_time, end_time], callback=self.on_success)
    def on_success(self, resp):
        self.write(resp.result)
        self.finish()