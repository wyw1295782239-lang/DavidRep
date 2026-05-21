import pymysql
from config import Config
def conn():
    con = pymysql.connect(host=Config.HOST,port=Config.PORT,
                          user=Config.USER,password=Config.PASSWORD,db=Config.DATABASE)
    cur =con.cursor()
    return con,cur

def close():
    con,cur = conn()
    cur.close()
    con.close()


#查询
def query(sql):
    con,cur = conn()
    cur.execute(sql)
    res=cur.fetchall()
    return res
