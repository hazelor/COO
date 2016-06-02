__author__ = 'guoxiao'

from base import base_handler
import tornado
import redis,json
from util.confs import *
from util.commons import *
from util.dbtool import *


class setting_handler(base_handler):
    @tornado.web.authenticated
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
        mac_address_list = (self.current_user).strip().split(',')
        g_interval_conf=[]
        for item in mac_address_list:
            sql = "select mac_address,location,duration from device where mac_address='%s' " % (item)
            with database_resource() as cursor:
                cursor.execute(sql)
                data = cursor.fetchall()
            if data:
                # data[0]=str(data[0])
                g_interval_conf += data
        return self.render('setting.html',
                           page_name = 'settings',
                           sub_page_name = 'basic',
                           devices_info = g_interval_conf
                           )

    def interval_setting(self):
        contents = self.get_argument('setting_content', '')
        j_contents = json.loads(contents)
        for j_c in j_contents:
            mac_address = j_c['mac_address'].strip()
	    # print mac_address
	    # mac_address = get_md5(mac_address)
            interval = j_c['interval']
            if mac_address != '' and interval != '':
                # r=redis.Redis()
                # r.hmset(mac_address, {'interval':interval})
                sql = "UPDATE `device` SET `duration` = '%s' WHERE `device`.`mac_address` = '%s' "%(interval, mac_address)
                with database_resource() as cursor:
                    cursor.execute(sql)
                # data = cursor.fetchall()
        self.write('Y')




class setting_basicModule(tornado.web.UIModule):
    def render(self):
        return self.render_string("setting_basic.html")

    # def embedded_javascript(self):
    #     basic_config_dict = {}
    # def on_su
    #     basic_config_dict['device_name'] = ''
    #     basic_config_dict['device_id'] = ''
    #     basic_config_dict['device_type'] = ''
    #     basic_config_dict['channel_number'] = ''
    #     basic_config_dict['storage'] = ''
    #     get_basic_conf_value(basic_config_dict)
    #     return self.render_string("setting_basic.js", device_name=basic_config_dict['device_name'],
    #                               device_id=basic_config_dict['device_id'], device_type=basic_config_dict['device_type'],
    #                               channel_number=basic_config_dict['channel_number'], storage=basic_config_dict['storage'], )
