import pymysql
from dao import DBConnection


def addDiary(content, loginId, date):
    conn = DBConnection.getConnection()
    try:
        cursor = conn.cursor()
        sql = "insert into diary(content, memberID, date) values(%s,%s,%s)"
        value=(content, loginId, date)
        cursor.execute(sql,value)
        data = cursor.fetchall()
        conn.commit()
        print("일기가 추가되었습니다")
    finally:
        conn.close()
    return ""

def getDiary(loginId):
    conn = DBConnection.getConnection()
    try:
        cursor = conn.cursor()
        sql = "select diary.date, emotion.emotionImg from diary, emotion where diary.emotionId = emotion.emotionId and diary.memberId = %s"
        cursor.execute(sql, loginId)
        row = cursor.fetchall()
        data_list=[]
        for obj in row:
            data_dic = {
                'date' : obj[0],
                'img' : obj[1]
            }
            data_list.append(data_dic)
    finally:
        conn.close()
    return data_list

