__author__ = 'guoxiao'
import os,time
import md5

def getPWDDir():
    return os.getcwd()

def create_nowTime_strip():
    return time.strftime('%Y%m%d%H%M%S', time.localtime())

def get_md5(raw_str):
    mdtool = md5.new()
    mdtool.update(raw_str)
    return mdtool.hexdigest()