__author__ = 'guoxiao'

try:
  import xml.etree.cElementTree as ET
except ImportError:
  import xml.etree.ElementTree as ET

from marcos import CHAMBER_CONF_PATH

def get_chambers_conf():
    try:
        tree = ET.parse(CHAMBER_CONF_PATH)
        root = tree.getroot()
    except Exception, e:
        print e
    chamber_conf = {}
    for chamber in root.findall('chamber'):
        ch_dict = {}
        key = chamber.get('key')
        name = chamber.get('name')
        ch_dict['name'] = name
        ch_dict['data_contents'] = {}
        data_contents = chamber.find('data_contents')
        for dc in data_contents.findall('data_content'):
            dc_key = dc.get('key')
            dc_name = dc.get('name')
            ch_dict['data_contents'][dc_key] = dc_name
        chamber_conf[key] = ch_dict
    return chamber_conf

def get_interval_conf():
    try:
        tree = ET.parse(CHAMBER_CONF_PATH)
        root = tree.getroot()
    except Exception, e:
        print e
    interval_list =[]
    for it in root.findall('interval'):
        it_dict = {}
        it_dict['key'] = it.get('key')
        it_dict['value'] = int(it.get('value'))
        interval_list.append(it_dict)
    return interval_list

g_chamber_conf = get_chambers_conf()

g_interval_conf = get_interval_conf()