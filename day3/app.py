import json
from flask import Flask, request, render_template,session,redirect,url_for,flash

app = Flask(__name__)
app.secret_key='id'

# 기본 페이지 접속
@app.route("/")
def index():
    return render_template("index.html")

# 화면 렌더링 함수
@app.route("/current")
def current():
    if(session['login']==False):
        return redirect(url_for("index"))
    else :
        return redirect(url_for("calendar"))


@app.route("/home_header")
def home_header():
    return render_template("home_header.html")

@app.route("/sign_in")
def sign_in():
    return render_template("sign_in.html")

@app.route("/sign_up")
def sign_up():
    return render_template("sign_up.html")
  
@app.route("/diary")
def diary():
    return render_template("keep_diary.html")

@app.route("/plan")
def plan():
    return render_template("make_plan.html")

@app.route("/calendar")
def calendar():
    diary_list = DiaryDAO.getDiary(session['login'])
    return render_template("calendar.html", data_list = diary_list)

@app.route("/logout")
def logout():
    session['login']=False
    return redirect(url_for("index"))

@app.route("/result_diary")
def result_diary():
    return render_template("result_diary.html")

@app.route("/result_plan")
def result_plan():
    return render_template("result_plan.html")

# DB 동작 함수

@app.route("/check_dup_chk", methods=['post'])
def check_dup_chk():
    isExist=0
    result="사용불가"
    data= request.get_json()
    print("[check_dup_chk: 받은 데이터]")
    print(data)
    # 만약 해당 objectId의 object가 존재하면 isExist = 1
    isExist = MemberDAO.isExist(data['objectId'], data['object'])
    if (isExist==0):
        print("사용가능한 " + data['objectId'][4:] + " 입니다!")
        result="사용가능"
    else:
        print("[사용불가]이미 존재하는 " + data['objectId'][4:] + " 입니다!")                                                
    return result

@app.route("/sign_in_check", methods=['post'])
def sign_in_check():
    data = request.get_json()
    print(data)
    isLogin=False
    member={'id': data['loginId'], 'password' : data['loginPw']}
    isLogin = MemberDAO.login(member)
    if(isLogin!=False):
        session['login']=data['loginId']
        print(session['login'])
        print("로그인성공")
    else:
        print( "로그인 실패")  
    return ""

@app.route("/sign_up_check", methods=['post'])
def sign_up_check():
    data = request.get_json()
    member = {'id': data['userId'], 'password' : data['userPw'], 'name':data['userName'], 'email' : data['userEmail']}
    MemberDAO.signup(member)
    return ""

@app.route("/diary_check", methods=['POST'])
def diary_check():
    data = request.get_json()
    print(data);
    DiaryDAO.addDiary(data['diarycontent'], session['login'],data['date'])
    return ""

@app.route("/plan_check", methods=['post'])
def plan_check():
    data = request.get_json()
    print(data)
    PlanDAO.addPlan(data['plancontent'], session['login'],data['date'])
    return ""

    
if __name__ =='__main__':
    app.run(host='0.0.0.0')
