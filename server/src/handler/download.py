__author__ = 'guoxiao'


from base import base_handler
# from util.commons import *
from util.confs import *
# from util.marcos import DOWNLOAD_DIR
# import os
import tornado
# import json
import tcelery
import tasks
import time


tcelery.setup_nonblocking_producer()

class download_handler(base_handler):
    @tornado.web.asynchronous
    def get(self, *args, **kwargs):
        is_file_download = self.get_argument('is_file_download', False)
        if not is_file_download:

            return self.get_download_page()
        else:
            start_time=self.get_argument('start_time')+':00'
            start_time = time.mktime(time.strptime(start_time, '%Y-%m-%d %H:%M:%S'))
            end_time=self.get_argument('end_time')+':00'
            end_time = time.mktime(time.strptime(end_time, '%Y-%m-%d %H:%M:%S'))
            return self.get_download_file(start_time, end_time)
    def get_download_page(self):
        return self.render('download.html',
                           page_name = 'download',
                           )

    def get_download_file(self, start_time, end_time):
        tasks.data_zip.apply_async(args=[start_time, end_time], callback=self.on_success)

    def on_success(self, resp):
        print '----------------',resp.result
        self.write(resp.result)
        self.finish()

