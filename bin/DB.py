import sys,os

sys.path.append(os.path.abspath('./conf/'))

import MySQLdb
from conf import DB

def getConn():
    try:
        return MySQLdb.connect(host=DB.HOST,user=DB.USER,passwd=DB.PASSWD,db=DB.NAME,charset=DB.CHARSET);
    except MySQLdb.Error,e:
        print "MySQLdb Error %d,%s" %(e.args[0],e.args[1])

def batchSQL(sql='',list=[],trun=''):
    conn = getConn()
    cur = conn.cursor()
    if trun:
        cur.execute(trun)
    for l in list:
        cur.execute(sql,l)
