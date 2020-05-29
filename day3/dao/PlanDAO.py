import pymysql
from dao import DBConnection

def addPlan(content, loginId, date):
    conn = DBConnection.getConnection()
    try:
        cursor = conn.cursor()
        sql = "insert into plan(content, memberID, date) values(%s,%s,%s)"
        value=(content, loginId, date)
        cursor.execute(sql,value)
        data = cursor.fetchall()
        conn.commit()
        print("계획이 추가되었습니다")
    finally:
        conn.close()
    return ""
