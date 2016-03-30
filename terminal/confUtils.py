__author__ = 'guoxiao'

from macros import *
import copy, ConfigParser


def get_update_duration():
    cr = ConfigParser.RawConfigParser()
    cr.read("./config.conf")
    return cr.getint("main", "update_duration")


def set_update_duration(duration):
    cr = ConfigParser.RawConfigParser()
    cr.read("./config.conf")
    cr.set("main", "update_duration", str(duration))
    cr.write(open("./config.conf","w"))


def get_dev_conf():
    pos1 = {'position': 1, 'contents':[]}
    name_list = [TARGET_CONCENTRATION, MEASURED_CONCENTRATION, AIR_TEMPERATURE, AIR_HUMIDITY, SOIL_TEMPERATURE, SOIL_HUMIDITY,MEASURED_CONCENTRATION_AVG_20S,CALIBRATE_CONCENTRATION]
    start_pos_list = [0, 4, 40, 60, 80, 88,104,124]
    para = {'name':TARGET_CONCENTRATION, 'start_pos': 0, 'length': 4, 'type': 'float'}

    for i in range(len(name_list)):
        para = copy.copy(para)
        para['name'] = name_list[i]
        para['start_pos'] = start_pos_list[i]

        pos1['contents'].append(para)

    pos2 = {'position': 2, 'contents': []}
    name_list = [TARGET_CONCENTRATION, MEASURED_CONCENTRATION, AIR_TEMPERATURE, AIR_HUMIDITY, MEASURED_CONCENTRATION_AVG_20S, CALIBRATE_CONCENTRATION]
    start_pos_list = [8, 12, 44, 64,108,128]
    for i in range(len(name_list)):
        para = copy.copy(para)
        para['name'] = name_list[i]
        para['start_pos'] = start_pos_list[i]
        i
        pos2['contents'].append(para)

    pos3 = {'position': 3, 'contents': []}
    name_list = [TARGET_CONCENTRATION, MEASURED_CONCENTRATION, AIR_TEMPERATURE, AIR_HUMIDITY,MEASURED_CONCENTRATION_AVG_20S, CALIBRATE_CONCENTRATION]
    start_pos_list = [16, 20, 48, 68, 112, 132]
    for i in range(len(name_list)):
        para = copy.copy(para)
        para['name'] = name_list[i]
        para['start_pos'] = start_pos_list[i]

        pos3['contents'].append(para)

    pos4 = {'position': 4, 'contents': []}
    name_list = [TARGET_CONCENTRATION, MEASURED_CONCENTRATION, AIR_TEMPERATURE, AIR_HUMIDITY,MEASURED_CONCENTRATION_AVG_20S, CALIBRATE_CONCENTRATION]
    start_pos_list = [24, 28, 52, 72, 116, 136]
    for i in range(len(name_list)):
        para = copy.copy(para)
        para['name'] = name_list[i]
        para['start_pos'] = start_pos_list[i]

        pos4['contents'].append(para)

    pos5 = {'position': 5, 'contents': []}
    name_list = [MEASURED_CONCENTRATION, AIR_TEMPERATURE, AIR_HUMIDITY,SOIL_TEMPERATURE, SOIL_HUMIDITY,MEASURED_CONCENTRATION_AVG_30M, MEASURED_CONCENTRATION_AVG_20S, CALIBRATE_CONCENTRATION ]
    start_pos_list = [96, 56, 76, 84, 92,100,120,140]
    for i in range(len(name_list)):
        para = copy.copy(para)
        para['name'] = name_list[i]
        para['start_pos'] = start_pos_list[i]
        pos5['contents'].append(para)

    dev_conf = [pos1, pos2, pos3, pos4, pos5]

    return dev_conf



