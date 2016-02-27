__author__ = 'guoxiao'
import os,time

def getPWDDir():
    return os.getcwd()

def create_nowTime_strip():
    return time.strftime('%Y%m%d%H%M%S', time.localtime())
