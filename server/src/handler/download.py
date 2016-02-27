__author__ = 'guoxiao'


from base import base_handler
from util.commons import *
from util.confs import *
from util.marcos import DOWNLOAD_DIR
import os

class download_handler(base_handler):
    def get(self, *args, **kwargs):
        is_file_download = self.get_argument('is_file_download', False)
        if not is_file_download:
            return self.get_download_page()
        else:
            return self.get_download_file()
    def get_download_page(self):
        return self.render('download.html',
                           page_name = 'download',
                           )

    def get_download_file(self):
        folder_name = os.path.join(getPWDDir(),DOWNLOAD_DIR)
        file_name = create_nowTime_strip()+'.csv'
        file_path = os.path.join(folder_name, file_name)
        ##get the data for all

        return file_path

