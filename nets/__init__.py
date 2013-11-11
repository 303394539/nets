import MySQLdb as mysql
from nets.settings import DATABASE

def connect(usedict=False, **kwargs):
    DATABASE.update(kwargs)
    con = mysql.connect(**DATABASE)
    con.autocommit(True)
    if usedict:
        cur = con.cursor(mysql.cursors.DictCursor)
    else:
        cur = con.cursor()
    cur.execute('SET interactive_timeout=3*24*3600')
    cur.execute('SET wait_timeout=3*24*3600')
    return cur
