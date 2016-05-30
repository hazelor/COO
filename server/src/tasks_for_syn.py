# coding=utf-8
import os,sys
import redis
import mysql.connector
from celery import Celery,platforms
import json,time
from util.dbtool import *
from util.commons import *
from util.confs import *
import collections
import tornado
from schedule import *
import time

reload(sys)
sys.setdefaultencoding( "utf-8" )

@tornado.gen.coroutine
def db_save(jdatas):
    r=redis.Redis()
    db_name_prefix = ''
    with database_resource() as cursor:
        sql = "select `db_name_prefix` from `db_name_prefix` where id=1"
        cursor.execute(sql)
        result = cursor.fetchall()
        db_name_prefix = result[0][0]
    #print db_name_prefix
#    data_dict={'air_temperature':[],'air_humidity':[],'soil_temperature':[],'soil_humidity':[],'measured_concentration':[],'target_concentration':[], 'measured_concentration_avg_30m':[],'measured_concentration_avg_20s':[],'calibrate_concentration':[],'object_diff':[],'action_time':[],'backup1':[],'backup2':[]}
    data_dict={}
    for item in data_type_enum:
        data_dict[item]=[]
    if len(jdatas) != 0:
        for jdata in jdatas:
            mac_address=jdata['mac_address']
            date=jdata['date']
#            print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(date))
#            print date
            position=jdata['position']
            for k,v in jdata['data'].iteritems():
                if k in data_dict:
                    data_dict[k].append((mac_address, position, v, date))
                    r.hmset(mac_address+','+str(position)+','+k, {'date':date, 'value':v})
    with database_resource() as cursor:
        for key in data_dict.keys():
            try:
                cursor.executemany('insert into '+'`'+db_name_prefix+key+'`'+' (mac_address, position, value, date) values (%s, %s, %s, %s)', data_dict[key])
            except:
                continue
    raise tornado.gen.Return('Y')

@tornado.gen.coroutine
def db_query(mac_address, position, type, start_time, end_time):
    db_list=[]
    data=[[],[]]
    with database_resource() as cursor:
        sql = "select `start_time`,`end_time`,`name` from `db_map` WHERE `start_time`<=%s AND `end_time`>=%s AND `basic_name`='%s'"%(start_time,start_time,type)
        cursor.execute(sql)
        result_smaller = cursor.fetchall()
        db_list+=result_smaller
        print 'result_smaller'
        print result_smaller
        if len(result_smaller) != 0:
            if result_smaller[-1][1] < float(end_time):
                sql = "select `start_time`,`end_time`,`name` from `db_map` WHERE `start_time`<%s AND `end_time`>=%s AND `basic_name`='%s'"%(end_time,end_time,type)
                cursor.execute(sql)
                result_larger = cursor.fetchall()
                print 'result_larger'
                print result_larger
                if len(result_larger) != 0: 
                    if result_larger[-1][0] != result_smaller[-1][1]:
                        sql = "select `start_time`,`end_time`,`name` from `db_map` WHERE `start_time`>%s AND `end_time`<%s AND `basic_name`='%s'"%(start_time,end_time,type)
                        cursor.execute(sql)
                        result_between = cursor.fetchall()
                        print 'result_between'
                        print result_between
                        db_list+=result_between
                        db_list+=result_larger
                    else:
                        db_list+=result_larger
        print 'db_list'
        print db_list
        for item in db_list:
            sql = "select date,value from `%s` where mac_address='%s' and position=%s and date BETWEEN %s and %s" % (item[2], mac_address, position, start_time, end_time)
            cursor.execute(sql)
            result = cursor.fetchall()
            data[0] += result
        if len(data[0])==0:
            data[0]=''
        if type == 'measured_concentration_avg_20s':
            for item in db_list:
                sql = "select date,value from `%s` where mac_address='%s' and position=%s and date BETWEEN %s and %s" % (str(item[0])+'target_concentration', mac_address, position, start_time, end_time)
                cursor.execute(sql)
                result = cursor.fetchall()
                data[1] += result
        else:
            data[1]=''
    if data:
        raise tornado.gen.Return(data)
    else:
        raise tornado.gen.Return(None)


@tornado.gen.coroutine
def db_query_all(mac_address, position, type, start_time, end_time):
    data=[]
    query_list=[]
    db_name_prefix = ''
    with database_resource() as cursor:
        sql = "select `db_name_prefix` from `db_name_prefix` where id=1"
        cursor.execute(sql)
        result = cursor.fetchall()
        db_name_prefix = result[0][0]
    print db_name_prefix
    if position == '5':
#        query_list=['measured_concentration_avg_20s','measured_concentration_avg_30m','air_humidity','soil_humidity','air_temperature','soil_temperature','object_diff','action_time']
        query_list=db_query_all_list_if_position_is_five
    else:
#        query_list=['measured_concentration_avg_20s','target_concentration','air_humidity','soil_humidity','air_temperature','soil_temperature','object_diff','action_time']
        query_list=db_query_all_list_if_position_not_five
    with database_resource() as cursor:
        for i in xrange(0,len(query_list)):
            try:
                sql = "select date,value from `%s` where mac_address='%s' and position=%s and date BETWEEN %s and %s" % (db_name_prefix+query_list[i], mac_address, position, start_time, end_time)
                cursor.execute(sql)
                result=cursor.fetchall()
                data.append(result)
            except:
                continue
    raise tornado.gen.Return(data)
        

@tornado.gen.coroutine
def redis_query(mac_address, position):
#    type_list=[{'air_temperature':'空气温度'},{'air_humidity':'空气湿度'},{'soil_temperature':'土壤温度'},{'soil_humidity':'土壤湿度'},{'target_concentration':'目标浓度'},{'measured_concentration_avg_30m':'测量浓度5min均值'},{'measured_concentration_avg_20s':'测量浓度'},{'calibrate_concentration':'传感器校准值'},{'object_diff':'目标差值'},{'action_time':'通气时间'}]
#    data=[[],[[],[],[],[],[],[],[],[]]]
    data=[[],[]]
    r=redis.Redis()
    if position == '5':
        for i in xrange(0,len(db_query_all_list_if_position_is_five)):
            data[1].append([])
            data[1][i].append(r.hget(mac_address+','+position+','+db_query_all_list_if_position_is_five[i], 'date'))
            data[1][i].append(r.hget(mac_address+','+position+','+db_query_all_list_if_position_is_five[i], 'value'))
    else:
        for i in xrange(0,len(db_query_all_list_if_position_not_five)):
            data[1].append([])
            data[1][i].append(r.hget(mac_address+','+position+','+db_query_all_list_if_position_not_five[i], 'date'))
            data[1][i].append(r.hget(mac_address+','+position+','+db_query_all_list_if_position_not_five[i], 'value'))
#    r=redis.Redis()
#    data[1][0].append(r.hget(mac_address+','+position+','+'measured_concentration_avg_20s', 'date'))
#    data[1][0].append(r.hget(mac_address+','+position+','+'measured_concentration_avg_20s', 'value'))
#    if position == '5':
#        data[1][1].append(r.hget(mac_address+','+position+','+'measured_concentration_avg_30m', 'date'))
#        data[1][1].append(r.hget(mac_address+','+position+','+'measured_concentration_avg_30m', 'value'))    
#    else:
#        data[1][1].append(r.hget(mac_address+','+position+','+'target_concentration', 'date'))
#        data[1][1].append(r.hget(mac_address+','+position+','+'target_concentration', 'value'))
#    data[1][2].append(r.hget(mac_address+','+position+','+'air_humidity', 'date'))
#    data[1][2].append(r.hget(mac_address+','+position+','+'air_humidity', 'value'))
#    data[1][3].append(r.hget(mac_address+','+position+','+'soil_humidity', 'date'))
#    data[1][3].append(r.hget(mac_address+','+position+','+'soil_humidity', 'value'))
#    data[1][4].append(r.hget(mac_address+','+position+','+'air_temperature', 'date'))
#    data[1][4].append(r.hget(mac_address+','+position+','+'air_temperature', 'value'))
#    data[1][5].append(r.hget(mac_address+','+position+','+'soil_temperature', 'date'))
#    data[1][5].append(r.hget(mac_address+','+position+','+'soil_temperature', 'value'))
#    data[1][6].append(r.hget(mac_address+','+position+','+'object_diff', 'date'))
#    data[1][6].append(r.hget(mac_address+','+position+','+'object_diff', 'value'))
#    data[1][7].append(r.hget(mac_address+','+position+','+'action_time', 'date'))
#    data[1][7].append(r.hget(mac_address+','+position+','+'action_time', 'value'))
    for item in redis_query_type_list:
        for k,v in item.items():
            value = r.hget(mac_address+','+position+','+k, 'value')
            if value:
                data[0].append(v)
                data[0].append(value)
    raise tornado.gen.Return(data)

@tornado.gen.coroutine
def user_check(username, password):
    sql = "select * from user where username='%s' and password='%s' " % (username, password)
    with database_resource() as cursor:
        cursor.execute(sql)
        data = cursor.fetchall()
    if data:
        raise tornado.gen.Return(data)
    else:
        raise tornado.gen.Return(None)

@tornado.gen.coroutine
def device_query(username):
    sql = "select mac_address from device where username='%s' " % (username)
    with database_resource() as cursor:
        cursor.execute(sql)
        data = cursor.fetchall()
    if data:
        raise tornado.gen.Return(data)
    else:
        raise tornado.gen.Return(None)

@tornado.gen.coroutine
def db_query_basic(sql):
    with database_resource() as cursor:
        cursor.execute(sql)
        data = cursor.fetchall()
    if data:
        raise tornado.gen.Return(data)
    else:
        raise tornado.gen.Return(None)

@tornado.gen.coroutine
def interval_redis_query(mac_address):
    r=redis.Redis()
    data = r.hget(mac_address, 'interval')
    if data:
        raise tornado.gen.Return(data)
    else:
        raise tornado.gen.Return('')
