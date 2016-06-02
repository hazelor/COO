#!/usr/bin/python
#-*-coding:utf-8-*-
__author__ = 'guoxiao'

import collections

# try:
#   import xml.etree.cElementTree as ET
# except ImportError:
#   import xml.etree.ElementTree as ET
#
# from marcos import CHAMBER_CONF_PATH
#
# def get_chambers_conf():
#     try:
#         tree = ET.parse(CHAMBER_CONF_PATH)
#         root = tree.getroot()
#     except Exception, e:
#         print e
#     chamber_conf = {}
#     for chamber in root.findall('chamber'):
#         ch_dict = {}
#         key = chamber.get('key')
#         name = chamber.get('name')
#         ch_dict['name'] = name
#         ch_dict['data_contents'] = {}
#         data_contents = chamber.find('data_contents')
#         for dc in data_contents.findall('data_content'):
#             dc_key = dc.get('key')
#             dc_name = dc.get('name')
#             ch_dict['data_contents'][dc_key] = dc_name
#         chamber_conf[key] = ch_dict
#     return chamber_conf
#
# def get_interval_conf():
#     try:
#         tree = ET.parse(CHAMBER_CONF_PATH)
#         root = tree.getroot()
#     except Exception, e:
#         print e
#     interval_list =[]
#     for it in root.findall('interval'):
#         it_dict = {}
#         it_dict['key'] = it.get('key')
#         it_dict['value'] = int(it.get('value'))
#         interval_list.append(it_dict)
#     return interval_list
#
# g_chamber_conf = get_chambers_conf()
#
# g_interval_conf = get_interval_conf()
short_name_to_english_name=collections.OrderedDict()
short_name_to_english_name['ah']='air_humidity'
short_name_to_english_name['at']='air_temperature'
short_name_to_english_name['cc']='calibrate_concentration'
short_name_to_english_name['mc']='measured_concentration'
short_name_to_english_name['mcm']='measured_concentration_avg_30m'
short_name_to_english_name['mcs']='measured_concentration_avg_20s'
short_name_to_english_name['sh']='soil_humidity'
short_name_to_english_name['st']='soil_temperature'
short_name_to_english_name['tc']='target_concentration'
short_name_to_english_name['od']='object_diff'
short_name_to_english_name['act']='action_time'
short_name_to_chinese_name=collections.OrderedDict()
short_name_to_chinese_name['ah']='空气湿度'
short_name_to_chinese_name['at']='空气温度'
short_name_to_chinese_name['cc']='传感器校准值'
short_name_to_chinese_name['mc']='测量浓度'
short_name_to_chinese_name['mcm']='测量浓度5min均值'
short_name_to_chinese_name['mcs']='测量浓度20s均值'
short_name_to_chinese_name['sh']='土壤湿度'
short_name_to_chinese_name['st']='土壤温度'
short_name_to_chinese_name['tc']='目标浓度'
short_name_to_chinese_name['od']='目标差值'
short_name_to_chinese_name['act']='通气时间'

data_type_enum=['air_temperature', 'air_humidity', 'soil_temperature', 'soil_humidity', 'measured_concentration', 'target_concentration', 'measured_concentration_avg_30m', 'measured_concentration_avg_20s', 'calibrate_concentration', 'object_diff', 'action_time']

db_query_all_list_if_position_is_five=['measured_concentration_avg_20s','measured_concentration_avg_30m','air_humidity','soil_humidity','air_temperature','soil_temperature','object_diff','action_time']

db_query_all_list_if_position_not_five=['measured_concentration_avg_20s','target_concentration','air_humidity','soil_humidity','air_temperature','soil_temperature','object_diff','action_time']

redis_query_type_list=[{'air_temperature':'空气温度'},{'air_humidity':'空气湿度'},{'soil_temperature':'土壤温度'},{'soil_humidity':'土壤湿度'},{'target_concentration':'目标浓度'},{'measured_concentration_avg_30m':'测量浓度5min均值'},{'measured_concentration_avg_20s':'测量浓度'},{'calibrate_concentration':'传感器校准值'},{'object_diff':'目标差值'},{'action_time':'通气时间'}]
