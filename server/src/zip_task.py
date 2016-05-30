#!/usr/bin/python
# -*- coding:utf-8 -*-
import os,sys
import redis
import mysql.connector
import json,time
from util.dbtool import *
from util.commons import *
from util.confs import *
import collections
import time
from apscheduler.schedulers.blocking import BlockingScheduler

reload(sys)
sys.setdefaultencoding( "utf-8" )

def data_zip_by_category():
    mac_address_list=['81fa847dfd40170b6b87c51e7be57c87','98cc339e733ce601b4f31f99c31a71aa']
    start_time=str(int(time.time()//86400*86400-28800))
    end_time = str(int(start_time)+86400)
    category_file_list = []
    db_list=[]
    local_time=time.localtime(int(start_time))
    file_dir = os.path.join(getPWDDir(),DOWNLOAD_DIR)
    with database_resource() as cursor:
        # query db_list
        sql = "select `start_time`,`end_time`,`name` from `db_map` WHERE `start_time`<=%s AND `end_time`>%s AND `basic_name`='%s'"%(start_time,start_time,'air_humidity')
        cursor.execute(sql)
        result_smaller = cursor.fetchall()
        db_list+=result_smaller
        print 'result_smaller'
        print result_smaller
        if len(result_smaller) != 0:
            if result_smaller[-1][1] < int(end_time):
                sql = "select `start_time`,`end_time`,`name` from `db_map` WHERE `start_time`<%s AND `end_time`>=%s AND `basic_name`='%s'"%(end_time,end_time,'air_humidity')
                cursor.execute(sql)
                result_larger = cursor.fetchall()
                print 'result_larger'
                print result_larger
                if len(result_larger) != 0:
                    if result_larger[-1][0] != result_smaller[-1][1]:
                        sql = "select `start_time`,`end_time`,`name` from `db_map` WHERE `start_time`>%s AND `end_time`<%s AND `basic_name`='%s'"%(start_time,end_time,'air_humidty')
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
    for k,category_name in short_name_to_english_name.items():
        for mac_address in mac_address_list:
            index=1
            file_list=[]
            with database_resource() as cursor:
                sql="select location from device WHERE mac_address='%s' "%(mac_address)
                cursor.execute(sql)
                mac_address_name=cursor.fetchone()
                if category_name == 'measured_concentration_avg_30m':
                    category_file_path=os.path.join(file_dir,mac_address_name[0]+'measured_concentration_avg_5m'+'.csv')
                else:
                    category_file_path=os.path.join(file_dir,mac_address_name[0]+category_name+'.csv')
                category_file_list.append(category_file_path)
                sql="select position from %s_%s WHERE mac_address='%s' "%(category_name, 'member', mac_address)
                cursor.execute(sql)
                positions = cursor.fetchall()
            for position in positions:
                file_path=os.path.join(file_dir,mac_address_name[0]+category_name+'-%d.csv'%(index))
                file_list.append(file_path)
                index+=1
                mac_address_position = ','.join([mac_address,position[0]])
                with database_resource() as cursor:
                    datas=[]
                    sql="select name from air_chamber WHERE mac_address_position='%s' "%(mac_address_position)
                    cursor.execute(sql)
                    name=cursor.fetchone()
                    for i in xrange(len(db_list)):
                        try:
                            if db_list[i][0]==0:
                                sql="select date,value from %s WHERE mac_address='%s' and position='%s' and date BETWEEN %s AND %s "%(category_name, mac_address, position[0], start_time, end_time)
                            else:
                                sql="select date,value from %s WHERE mac_address='%s' and position='%s' and date BETWEEN %s AND %s "%(str(db_list[i][0])+category_name, mac_address, position[0], start_time, end_time)
                            cursor.execute(sql)
                            datas+=cursor.fetchall()
                        except:
                            continue
                f= open(file_path,'w+')
                if datas:
                    line_list=[]
                    line_list.append("%s,%s,\n" %("date time", name[0]))
                    for data in datas:
                        line_list.append("%s,%f,\n" %(time.strftime("%Y-%m-%d %X", time.localtime(data[0])), data[1]))
                    f.writelines(line_list)
                f.flush()
                f.close()
            # merge file
            cmd='paste'
            for p in file_list:
                cmd=cmd+' '+p
            cmd=cmd+'|cat > '+category_file_path
            os.system(cmd)
            cmd='rm '
            rm_file_path=os.path.join(file_dir,mac_address_name[0]+category_name+'-')
            cmd=cmd+rm_file_path+'*'
            os.system(cmd)
    zip_file_name = "%d_%d_%d.zip" %(local_time.tm_year, local_time.tm_mon, local_time.tm_mday)
    zip_file_path = os.path.join(file_dir, zip_file_name)
    zip_files_name = DOWNLOAD_DIR +'/*.csv'
    cmd = "zip %s %s" %(zip_file_path, zip_files_name)
    os.system(cmd)
    cmd = "rm %s" %(zip_files_name)
    os.system(cmd)


if __name__=='__main__':
#    data_zip_by_category()
    sched = BlockingScheduler()
    # sched.daemonic = False
    sched.add_job(data_zip_by_category, trigger='cron', hour='1')
    # sched.add_job(schedule_job, 'interval', seconds=3)
    try:
        sched.start()
    except (KeyboardInterrupt, SystemExit):
        pass
