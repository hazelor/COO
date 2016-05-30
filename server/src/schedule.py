# coding = utf-8
from apscheduler.schedulers.blocking import BlockingScheduler
import time
import redis
from util.dbtool import *
from util.confs import *

INTERVAL = 1

# scheduler = Scheduler(daemonic = False)

# @scheduler.cron_schedule(hour='0')
def schedule_job():
    start_time = int((time.time())//86400*86400-28800+86400)
    end_time = start_time + 86400*INTERVAL
    db_name_prefix = str(start_time)
    for db_name in data_type_enum:
        db_full_name = db_name_prefix + db_name
        # print db_full_name
        with database_resource() as cursor:
            sql = "DROP TABLE IF EXISTS %s"%(db_full_name)
            cursor.execute(sql)
            # print sql
            sql = "CREATE TABLE `%s` (\
                     `id` int(11) NOT NULL AUTO_INCREMENT,\
                     `mac_address` varchar(32) DEFAULT NULL,\
                     `position` varchar(20) DEFAULT NULL,\
                     `value` float DEFAULT NULL,\
                     `date` double NOT NULL,\
                     PRIMARY KEY (`id`),\
                     KEY `mac_address` (`mac_address`)\
                   ) ENGINE=InnoDB DEFAULT CHARSET=utf8"%(db_full_name)
            cursor.execute(sql)
            sql = "select `id` from `db_map` WHERE `start_time`=%d AND `end_time`=%d AND `name`='%s'"%(start_time,end_time,db_full_name)
            cursor.execute(sql)
            result = cursor.fetchall()
            if len(result) == 0:
                sql = "insert into `db_map`(`start_time`,`end_time`,`name`,`basic_name`) values\
                   (%d,%d,'%s','%s')"%(start_time,end_time,db_full_name,db_name)
                cursor.execute(sql)
    # r=redis.Redis()
    # r.set('db_name_prefix',db_name_prefix)
    with database_resource() as cursor:
        sql = "update `db_name_prefix` set `db_name_prefix`='%s'WHERE id=1"%(db_name_prefix)
        cursor.execute(sql)
    return

# scheduler.start()


if __name__ == '__main__':
    sched = BlockingScheduler()
    # sched.daemonic = False
    sched.add_job(schedule_job, trigger='cron', hour='0')
    # sched.add_job(schedule_job, 'interval', seconds=3)
    try:
        sched.start()
    except (KeyboardInterrupt, SystemExit):
        pass
#    schedule_job()
