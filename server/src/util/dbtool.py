import mysql.connector
from marcos import *


def create_engine(user, password, database, is_auto_commit=False, host='127.0.0.1', port=3306, **kw):
    params = dict(user=user, password=password, database=database, host=host,port=port)
    defaults = dict(use_unicode=True, charset='utf8', collation='utf8_general_ci', autocommit=is_auto_commit)
    for k,v in defaults.iteritems():
        params[k]=kw.pop(k,v)
    params.update(kw)
    params['buffered']=True
    engine = mysql.connector.connect(**params)
    return engine


class database_resource:
    def __enter__(self):
        self.conn = create_engine(DB_USER, DB_USER_PASSWORD, DB_NAME, is_auto_commit=False)
        self.cursor = self.conn.cursor()
        return self.cursor
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
