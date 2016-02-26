__author__ = 'guoxiao'

from base import base_handler

class preview_handler(base_handler):
    def get(self, *args, **kwargs):
        chambers = []
        return self.render('preview.html',
                           page_name = 'preview',
                           chambers = chambers,
                           )

