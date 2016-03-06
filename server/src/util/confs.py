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
short_name_to_english_name['mc']='measured_concentration'
short_name_to_english_name['sh']='soil_humidity'
short_name_to_english_name['st']='soil_temperature'
short_name_to_english_name['tc']='target_concentration'
short_name_to_chinese_name=collections.OrderedDict()
short_name_to_chinese_name['ah']='空气湿度'
short_name_to_chinese_name['at']='空气温度'
short_name_to_chinese_name['mc']='测量浓度'
short_name_to_chinese_name['sh']='土壤湿度'
short_name_to_chinese_name['st']='土壤温度'
short_name_to_chinese_name['tc']='目标浓度'

# short_name_to_english_name = {'ah':'air_humidity','at':'air_temperature','mc':'measured_concentration','sh':'soil_humidity','st':'soil_temperature','tc':'target_concentration'}
# short_name_to_chinese_name = {'ah':'空气湿度','at':'空气温度','mc':'测量浓度','sh':'土壤湿度','st':'土壤温度','tc':'目标浓度'}