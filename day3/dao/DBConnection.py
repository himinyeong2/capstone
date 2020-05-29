import pymysql
import json

def getConnection():
    return pymysql.connect(host='49.50.173.223', user='root', password='Admy106879!',
                           db='dayspirit',charset='utf8')
