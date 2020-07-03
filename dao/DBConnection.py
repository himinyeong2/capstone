import pymysql

def getConnection():
    return pymysql.connect(host='localhost', user='root', password='secret',
                           db='dayspirit',charset='utf8')
