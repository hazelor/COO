__author__ = 'guoxiao'


from base import base_handler

class download_handler(base_handler):
    def get(self, *args, **kwargs):
        return self.render('download.html',
                           page_name = 'download',
                           )
