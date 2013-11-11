import sys,os

sys.path.append(os.path.abspath('../bin/'))

from reference import Reference as ref

DB = ref(
    NAME = 'nets',
    USER = 'movie',
    PASSWD = 'movie',
    HOST = 'localhost',
    POST = 3306,
    CHARSET = 'utf8',
    BATCH = 50
)
if __name__=='__main__':
    print DB.NAME
