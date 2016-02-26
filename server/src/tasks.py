import os
import mysql.connector
from celery import Celery,platforms
# import json
from util.dbtool import *


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
    data_dict={'air_temperature':[],'air_humidity':[],'soil_temperature':[],'soil_humidity':[],'measured_concentration':[],'target_concentration':[]}
    if len(jdatas) != 0:
	for jdata in jdatas:
	    mac_address=jdata['mac_address']
	    date=jdata['date']
	    position=jdata['position']
    	    for k,v in jdata['data'].iteritems():
		data_dict[k].append((mac_address, position, v, date))
    with database_resource() as cursor:
	cursor.executemany('insert into air_temperature (mac_address, position, value, date) values (%s, %s, %s, %s)', data_dict['air_temperature'])
	cursor.executemany('insert into air_humidity (mac_address, position, value, date) values (%s, %s, %s, %s)', data_dict['air_humidity'])
	cursor.executemany('insert into soil_temperature (mac_address, position, value, date) values (%s, %s, %s, %s)', data_dict['soil_temperature'])
	cursor.executemany('insert into soil_humidity (mac_address, position, value, date) values (%s, %s, %s, %s)', data_dict['soil_humidity'])
	cursor.executemany('insert into measured_concentration (mac_address, position, value, date) values (%s, %s, %s, %s)', data_dict['measured_concentration'])
	cursor.executemany('insert into target_concentration (mac_address, position, value, date) values (%s, %s, %s, %s)', data_dict['target_concentration'])
    return 'Y'


if __name__ == "__main__":
    celery.start()
