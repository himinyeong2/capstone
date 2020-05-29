import pymysql

app = Flask(__name__)


def getConnection():
    return pymysql.connect(host='3.34.63.220', user='minyeong', password='minyeong',
                           db='dayspirit',charset='utf8')

@app.route("/")
def index():
    conn = getConnection()
    if(conn==False):
        return("실패")
    else:
        return("성공")
    
    
    

if __name__ =='__main__':
    app.run(host='0.0.0.0')
