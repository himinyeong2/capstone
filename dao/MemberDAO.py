import pymysql
from dao import DBConnection



def isExist(objectType, objectItem):
    cnt=0
    conn = DBConnection.getConnection()
    try:
        cursor = conn.cursor()
        if objectType=="userId" :
            sql = "select * from member where id = %s"
        elif objectType == "userEmail" :
            sql = "select * from member where email= %s"
        cursor.execute(sql, objectItem)
        data = cursor.fetchall()
        # 만약 아이디가 기존에 존재하면 cnt++
        for i in data:
            cnt = cnt+1
    finally:
        conn.close()
    
    # isExist = 0 이면 존재하지 않는 아이디이기 때문에 회원가입 가능
    return cnt

def findInfo(findType, obj1, obj2):
    
    conn = DBConnection.getConnection()
    find=False
    try:
        cursor = conn.cursor()
        if findType == "ID":
            sql = "select id from member where name=%s and email=%s "
        else :
            sql = "select password from member where id=%s and email= %s"
        value=(obj1,obj2)
        cursor.execute(sql, value)
        data = cursor.fetchall()
        for i in data:
            find=i[0]
    finally:
        conn.close()
        
    print(find)
    return find


def login(member):
    name = False;
    cnt=0
    conn = DBConnection.getConnection()
    cursor = conn.cursor()
    sql = "select name from member where id=%s and password=%s"
    value=(member['id'], member['password'])
    cursor.execute(sql, value)
    data = cursor.fetchall()
    for i in data:
        cnt = cnt+1
    conn.close()
    
    return cnt


def signup(member):
    conn = DBConnection.getConnection()
    try:
        cursor = conn.cursor()
        sql = "insert into member values(%s, %s, %s, %s)"
        value = (member['id'], member['password'], member['name'], member['email'])
        cursor.execute(sql,value)
        data = cursor.fetchall()
        conn.commit()
    finally:
        conn.close()
    return ""
