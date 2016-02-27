__author__ = 'sonic-server'

from handler import *
handlers = [
    (r'/', home_handler),
    (r'/preview',preview_handler),
    (r'/download',download_handler),
    (r'/history',history_handler),
    (r'/setting',setting_handler),
    (r"/setting/(\w+)",setting_handler),
    (r'/api/dataChannel', data_handler),
    (r'/api/ctrl', ctrl_handler)
]

modules = {
}
