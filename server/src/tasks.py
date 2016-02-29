# coding=utf-8
import os,sys
import redis
import mysql.connector
from celery import Celery,platforms
import json,time
from util.dbtool import *
from util.commons import *
from util.confs import *

reload(sys)
sys.setdefaultencoding( "utf-8" )

celery = Celery("tasks", broker="amqp://")
celery.conf.CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'amqp')
# celery.conf.update(
#     CELERY_TASK_SERIALIZER='json',
#     CELERY_ACCEPT_CONTENT=['json'],
#     CELERY_RESULT_SERIALIZER ='json',
# )
platforms.C_FORCE_ROOT = True

@celery.task(name='handler.tasks.db_save')
def db_save(jdatas):
    r=redis.Redis()
    data_dict={'air_temperature':[],'air_humidity':[],'soil_temperature':[],'soil_humidity':[],'measured_concentration':[],'target_concentration':[]}
    if len(jdatas) != 0:
        for jdata in jdatas:
            mac_address=jdata['mac_address']
            date=jdata['date']
            position=jdata['position']
            for k,v in jdata['data'].iteritems():
                data_dict[k].append((mac_address, position, v, date))
                r.hmset(mac_address+','+str(position)+','+k, {'date':date, 'value':v})
    with database_resource() as cursor:
        cursor.executemany('insert into air_temperature (mac_address, position, value, date) values (%s, %s, %s, %s)', data_dict['air_temperature'])
        cursor.executemany('insert into air_humidity (mac_address, position, value, date) values (%s, %s, %s, %s)', data_dict['air_humidity'])
        cursor.executemany('insert into soil_temperature (mac_address, position, value, date) values (%s, %s, %s, %s)', data_dict['soil_temperature'])
        cursor.executemany('insert into soil_humidity (mac_address, position, value, date) values (%s, %s, %s, %s)', data_dict['soil_humidity'])
        cursor.executemany('insert into measured_concentration (mac_address, position, value, date) values (%s, %s, %s, %s)', data_dict['measured_concentration'])
        cursor.executemany('insert into target_concentration (mac_address, position, value, date) values (%s, %s, %s, %s)', data_dict['target_concentration'])
    return 'Y'

@celery.task(name='handler.tasks.db_query')
def db_query(mac_address, position, type, start_time, end_time):
    sql = "select date,value from %s where mac_address='%s' and position=%s and date BETWEEN %s and %s" % (type, mac_address, position, start_time, end_time)
    with database_resource() as cursor:
        cursor.execute(sql)
        data = cursor.fetchall()
    if data:
        #data = json.dumps(data)
        return data
    # return sql


@celery.task(name='handler.tasks.redis_query')
def redis_query(mac_address, postion):
    type_list=[{'air_temperature':'空气温度'},{'air_humidity':'空气湿度'},{'soil_temperature':'土壤温度'},{'soil_humidity':'土壤湿度'},{'measured_concentration':'测量浓度'},{'target_concentration':'目标浓度'}]
    data=[[],[[],[]]]
    r=redis.Redis()
    mac_address = get_md5(mac_address)
    data[1][0].append(r.hget(mac_address+','+postion+','+'measured_concentration', 'date'))
    data[1][0].append(r.hget(mac_address+','+postion+','+'measured_concentration', 'value'))
    data[1][1].append(r.hget(mac_address+','+postion+','+'target_concentration', 'date'))
    data[1][1].append(r.hget(mac_address+','+postion+','+'target_concentration', 'value'))
    # data = json.dumps(data)
    for item in type_list:
        for k,v in item.items():
            value = r.hget(mac_address+','+postion+','+k, 'value')
            if value:
                data[0].append(v)
                data[0].append(value)
    return data

@celery.task(name='handler.tasks.data_zip')
def data_zip(start_time, end_time):
    chamber_file_list = []
    for k, v in g_chamber_conf.items():
        mac_address = get_md5(k.strip().split(',')[0])
        position = int(k.split(',')[1])
        chamber_name = v['name']
        file_dir = os.path.join(getPWDDir(),DOWNLOAD_DIR)
        index = 1
        file_list = []
        chamber_file_path = os.path.join(file_dir,chamber_name+'.csv')
        chamber_file_list.append(chamber_file_path)

        for type, name in v['data_contents'].items():
            data = db_query(mac_address, position, type, start_time, end_time)
            file_path = os.path.join(file_dir,chamber_name+'_%d.csv' % (index))
            print file_path
            file_list.append(file_path)
            f= open(file_path,'w+')
            index += 1
            if data:
                line_list = []
                line_list.append("%s,%s,\n" %(name, "date time"))
                for d in data:
                    line_list.append("%f,%s,\n" % (d[1],time.asctime(time.localtime(d[0]))))
                f.writelines(line_list)

        #merge the files
        cmd = "paste"
        for p in file_list:
            cmd = cmd +" " + p
        cmd = cmd +'|cat > ' + chamber_file_path
        print cmd
        os.system(cmd)
        cmd = "rm "
        rm_files_path = os.path.join(file_dir, chamber_name +'_')
        cmd = cmd + rm_files_path + "*"
        os.system(cmd)
    local_time = time.localtime(time.time())
    zip_file_name = "data_%d_%d_%d_%d_%d_%d.zip" %(local_time.tm_year, local_time.tm_mon, local_time.tm_mday, local_time.tm_hour, local_time.tm_min, local_time.tm_sec)
    zip_file_path = os.path.join(file_dir, zip_file_name)
    zip_files_name = DOWNLOAD_DIR +'/*.csv'
    cmd = "zip %s %s" %(zip_file_path, zip_files_name)
    os.system(cmd)
    cmd = "rm %s" %(zip_files_name)
    os.system(cmd)
    return zip_file_name

# @celery.task(name='handler.tasks.interval_redis_save')
# def interval_redis_save(mac_address, interval):
#     r=redis.Redis()
#     r.hmset(mac_address, {'interval':interval})
#     return 'Y'

@celery.task(name='handler.tasks.interval_redis_query')
def interval_redis_query(mac_address):
    r=redis.Redis()
    data = r.hget(mac_address, 'interval')
    if data:
        return data
    else:
        return ''



if __name__ == "__main__":
    celery.start()