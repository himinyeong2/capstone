import json
import pymysql
from dao import DBConnection


def manipulate_diary(_type, loginId, date, content, emotionId, emotion_list):

    conn = DBConnection.getConnection()
    try:
        cursor = conn.cursor()
        if _type=="EDIT":
            sql = "update diary set content=%s,emotionId=(select emotionId from emotion where emotionName=%s),items=%s where memberId=%s and date=%s"
            value = (content, emotionId, emotion_list,loginId, date)
        else:
            sql = "delete from diary where memberId=%s and date=%s"
            value=(loginId, date)
        cursor.execute(sql,value)
        data = cursor.fetchall()
        conn.commit()
    finally:
        conn.close()
    return ""
    

def addDiary(content, loginId, date,emotionId, emotion_list):
    conn = DBConnection.getConnection()
    try:
        cursor = conn.cursor()
        sql = "insert into diary(content, memberID, date,emotionId,items) values(%s,%s,%s,(select emotionId from emotion where emotionName=%s),%s)"
        value=(content, loginId, date,emotionId,emotion_list)
        cursor.execute(sql,value)
        data = cursor.fetchall()
        conn.commit()
        print("일기가 추가되었습니다")
    finally:
        conn.close()
    return ""

def isExistDiary(date, loginId):
    content=False
    conn = DBConnection.getConnection()
    try:
        cursor = conn.cursor()
        sql="select content from diary where date=%s and memberId=%s"
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


            
def getEmotion(date, loginId):
    conn = DBConnection.getConnection()
    find=False;
    try:
        cursor = conn.cursor()
        sql = "select emotionName,items from emotion, diary where emotion.emotionId=diary.emotionId and diary.date=%s and diary.memberId=%s"
        value=(date, loginId)
        cursor.execute(sql,value)
        row = cursor.fetchall()
    
        for obj in row:
            data_dic={
                'emotionName':obj[0],
                'items' : obj[1]
            }
    finally:
        conn.close()
    return data_dic
