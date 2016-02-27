__author__ = 'guoxiao'

from base import base_handler

class history_handler(base_handler):
    def get(self, *args, **kwargs):
        return self.render('history.html',
                           page_name = 'history',
                           )