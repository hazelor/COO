#!/usr/bin/env python
#--coding:utf-8--

__author__ = 'guoxiao'



ISOTIMEFORMAT = "%Y-%m-%d-%H-%M-%S"
AIR_HUMIDITY = "air_humidity" #空气湿度
AIR_TEMPERATURE = "air_temperature" #空气温度
SOIL_HUMIDITY = "soil_humidity" #土壤湿度
SOIL_TEMPERATURE = "soil_temperature" #土壤温度
MEASURED_CONCENTRATION = "measured_concentration" #测量浓度
TARGET_CONCENTRATION = "target_concentration" #目标浓度


SERVER_URL = "123.57.60.239"
UPDATE_PORT = "8080"

API_DATACHANNEL_URL = "/api/dataChannel"
API_CTRL_URL = "/api/ctrl"


SERIAL_PORT_NAME = '/dev/ttyS1'
SERIAL_PORT_BAUD = 9600
SERIAL_PORT_TIMEOUT = 0.5

RES_SUCCESS = 'Y'
RES_FAIL = 'N'

CTRL_UPDATE_DURATION = 10



