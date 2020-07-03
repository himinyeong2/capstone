import pymysql
from dao import DBConnection

def manipulate_plan(_type, loginId, date, content, keyword):
    conn = DBConnection.getConnection()
    month=int(date[5:7])
    try:
        cursor = conn.cursor()
        if _type=="EDIT":
            if(month>=3 and month <6):
                sql = "update plan set content=%s, colorId=(select color from spring where name=%s) where memberId=%s and date=%s"
            elif (month>=6 and month<9):
                sql = "update plan set content=%s, colorId=(select color from summer where name=%s) where memberId=%s and date=%s"
            elif (month >=9 and month <12):
                sql = "update plan set content=%s, colorId=(select color from fall where name=%s) where memberId=%s and date=%s"
            else:
                sql = "update plan set content=%s, colorId=(select color from winter where name=%s) where memberId=%s and date=%s"
            value = (content, keyword, loginId, date)
        else:
            sql = "delete from plan where memberId=%s and date=%s"
            value=(loginId, date)
        cursor.execute(sql,value)
        data = cursor.fetchall()
        conn.commit()
    finally:
        conn.close()
    return ""
    


def getColor(date, loginId):
    conn = DBConnection.getConnection()
    find=False;
    try:
        cursor = conn.cursor()
        sql = "select colorImg from color, plan where color.colorId=plan.colorId and plan.date=%s and plan.memberId=%s"
        value=(date, loginId)
        cursor.execute(sql, value)
        data = cursor.fetchall()
        for i in data:
            find = i[0]
    finally:
        conn.close()
    return find

def addPlan(content, loginId, date, keyword):
    conn = DBConnection.getConnection()
    month=int(date[5:7])
    try:
        cursor = conn.cursor()
        if(month>=3 and month <6):
            sql = "insert into plan(content, memberId, date, colorId) values(%s,%s,%s,(select color from spring where name=%s))"
        elif (month>=6 and month<9):
            sql = "insert into plan(content, memberId, date, colorId) values(%s,%s,%s,(select color from summer where name=%s))"
        elif (month >=9 and month <12):
            sql = "insert into plan(content, memberId, date, colorId) values(%s,%s,%s,(select color from fall where name=%s))"
        else:
            sql = "insert into plan(content, memberId, date, colorId) values(%s,%s,%s,(select color from winter where name=%s))"
            
        value=(content, loginId, date, keyword)
        cursor.execute(sql,value)
        data = cursor.fetchall()
        conn.commit()
        print("계획이 추가되었습니다")
    finally:
        conn.close()
    return ""

def isExistPlan(date, loginId):
    content=False
    conn = DBConnection.getConnection()
    try:
        cursor = conn.cursor()
        sql="select content from plan where date=%s and memberId=%s"
        value=(date, loginId)
        cursor.execute(sql, value)
        data = cursor.fetchall()
        # 만약 다이어리가 존재하면 cnt++
        for i in data:
            content=i[0]
    finally:
        conn.close()
    
    #다이어리가 존재하지 않으면 False를 반환
    return content    