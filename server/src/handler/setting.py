__author__ = 'guoxiao'

from base import base_handler
import tornado
import redis,json
from util.confs import *


class setting_handler(base_handler):
    def get(self, input = 'basic'):
        if input:
            sub_page_name = input
        else:
            sub_page_name = 'basic'
        if sub_page_name == 'basic':
            return self.render_basic()
        if sub_page_name == 'interval':
            self.interval_setting()

    def render_basic(self):
        return self.render('setting.html',
                           page_name = 'settings',
                           sub_page_name = 'basic',
                           )

    def interval_setting(self):
        contents = self.get_argument('setting_content', '')
        j_contents = json.loads(contents)
        for j_c in j_contents:
            mac_address = j_c['mac_address']
            interval = j_c['interval']
            if mac_address != '' and interval != '':
                r=redis.Redis()
                r.hmset(mac_address, {'interval':interval})
        self.write('Y')




class setting_basicModule(tornado.web.UIModule):
    def render(self):
        return self.render_string("setting_basic.html",devices_info = g_interval_conf)

    # def embedded_javascript(self):
    #     basic_config_dict = {}
    #     basic_config_dict['device_name'] = ''
    #     basic_config_dict['device_id'] = ''
    #     basic_config_dict['device_type'] = ''
    #     basic_config_dict['channel_number'] = ''
    #     basic_config_dict['storage'] = ''
    #     get_basic_conf_value(basic_config_dict)
    #     return self.render_string("setting_basic.js", device_name=basic_config_dict['device_name'],
    #                               device_id=basic_config_dict['device_id'], device_type=basic_config_dict['device_type'],
    #                               channel_number=basic_config_dict['channel_number'], storage=basic_config_dict['storage'], )

