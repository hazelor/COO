__author__ = 'sonic-server'

from handler import *
handlers = [
    (r'/', home_handler),
    (r'/api/dataChannel', data_handler),
    (r'/api/ctrl', ctrl_handler)
]

modules = {
}
