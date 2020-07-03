import json
from flask import Flask, request, render_template,session,redirect,url_for,flash
from dao import MemberDAO, DiaryDAO, PlanDAO
import model

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
  
@app.route("/find_id")
def find_id():
    return render_template("find_id.html")
@app.route("/find_pw")
def find_pw():
    return render_template("find_pw.html")
@app.route("/find_idpw")
def find_idpw():
    return render_template("find_idpw.html")

    
@app.route("/diary")
def diary():
    content=False
    date = request.args.get('date', "")
    content=DiaryDAO.isExistDiary(date, session['login'])
    if (content!=False):
        return render_template("keep_diary.html", tmp=content, data=date)
    else:
        return render_template("keep_diary.html", tmp="",data=date)

@app.route("/plan")
def plan():
    content=False
    date = request.args.get('date',"")
    content=PlanDAO.isExistPlan(date, session['login'])
    if (content!=False):
        return render_template("make_plan.html", tmp=content, data=date)
    else:
        return render_template("make_plan.html", tmp="",data=date)

@app.route("/calendar")
def calendar():
    diary_list = DiaryDAO.getDiary(session['login'])
    if len(diary_list)==0:
        return render_template("calendar.html")
    else:
        return render_template("calendar.html", data_list = diary_list)

@app.route("/logout")
def logout():
    session['login']=False
    return redirect(url_for("index"))

@app.route("/result_diary")
def result_diary():
    date = request.args.get('date', "")#2010-05-05
    emotion_list = DiaryDAO.getEmotion(date, session['login'])
    name = emotion_list['emotionName'] 
    emotion_items=json.loads(emotion_list['items'])#{"기쁘고 행복한": 37.6, "고요하고 편안한": 0.6, "화나고 적대적인": 37.9, "슬프고 불만족스러운": 11.0, "활기차고 사랑스러운": 12.8} => 딕셔너리 형태
    result_list=[]
    for i in emotion_items.items():
        data_dic={
            'name':i[0],
            'percent':i[1]
        }
        result_list.append(data_dic)
    return render_template("result_diary.html",data_list=result_list)

@app.route("/result_plan")
def result_plan():
    date=request.args.get('date',"")
    colorImg=PlanDAO.getColor(date,session['login'])
    return render_template("result_plan.html",tmp=colorImg)

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

@app.route("/check_find_id", methods=['post'])
def check_find_id():
    data=request.get_json()
    find_id = MemberDAO.findInfo("ID",data['userName'],data['userEmail'])
    if(find_id==False):
        find_id="이름 혹은 이메일이 옳지 않습니다."
    return find_id

@app.route("/check_find_pw", methods=['post'])
def check_find_pw():
    data=request.get_json()
    find_pw = MemberDAO.findInfo("PASSWORD", data['userId'], data['userEmail'])
    if(find_pw==False):
        find_pw = "아이디 혹은 이메일이 옳지 않습니다"
    return find_pw

@app.route("/sign_in_check", methods=['post'])
def sign_in_check():
    data = request.get_json()
    print(data)
    isLogin=False
    member={'id': data['loginId'], 'password' : data['loginPw']}
    isLogin = MemberDAO.login(member)
    if(isLogin!=False):
        session['login']=data['loginId']
        return "SUCCESS"
    else:
        return "FAILED"

@app.route("/sign_up_check", methods=['post'])
def sign_up_check():
    data = request.get_json()
    member = {'id': data['userId'], 'password' : data['userPw'], 'name':data['userName'], 'email' : data['userEmail']}
    MemberDAO.signup(member)
    return ""

def emotion_rank(emotion):
    pos = emotion['사랑/황홀/즐거움']+emotion['기쁨/낙천/기대']
    neg = emotion['분노/절망/짜증']+emotion['불안/슬픔/걱정']
    nor = emotion['평온/관심/수용']*2
    tmp = max(pos, neg, nor)
    if(tmp==pos):
        if(emotion['기쁨/낙천/기대']> emotion['사랑/황홀/즐거움']):
            result = "기쁨/낙천/기대"
        else:
            result = "사랑/황홀/즐거움"
    elif(tmp==neg):
        if(emotion['분노/절망/짜증']>emotion['불안/슬픔/걱정']):
            result="분노/절망/짜증"
        else:
            result="불안/슬픔/걱정"
    else:
        result="평온/관심/수용"
    return result
    

@app.route("/diary_check", methods=['POST'])
def diary_check():
    data = request.get_json()
    emotion_list=model.analyze_diary(data['diarycontent']) #활기차고 사랑스러운
    if emotion_list=="ERROR":
        return "ERROR"
    emotion = emotion_rank(emotion_list)
    DiaryDAO.addDiary(data['diarycontent'], session['login'],data['date'], emotion, json.dumps(emotion_list))
    return ""

@app.route("/diary_manipulate", methods=['post'])
def diary_manipulate():
    data= request.get_json()#type, content, date
    if data['type']=='EDIT':
        emotion_list = model.analyze_diary(data['diarycontent'])
        if emotion_list=="ERROR":
            return "ERROR"
        emotion=emotion_rank(emotion_list)
        DiaryDAO.manipulate_diary("EDIT", session['login'],data['date'],data['diarycontent'], emotion, json.dumps(emotion_list))
    else:
        DiaryDAO.manipulate_diary("DELETE", session['login'], data['date'],"","","")
    
    return "COMPLETE"
    


@app.route("/plan_check", methods=['post'])
def plan_check():
    data = request.get_json()
    plan_keyword=model.analyze_plan(data['plancontent'])
    PlanDAO.addPlan(data['plancontent'],session['login'],data['date'],plan_keyword)
    return ""

@app.route("/plan_manipulate", methods=['post'])
def plan_manipulate():
    data= request.get_json()#type, content, date
    if data['type']=='EDIT':
        plan_keyword = model.analyze_plan(data['plancontent'])
        if plan_keyword=="ERROR":
            return "ERROR"
        PlanDAO.manipulate_plan("EDIT", session['login'],data['date'],data['plancontent'], plan_keyword)
    else:
        PlanDAO.manipulate_plan("DELETE", session['login'], data['date'],"","")
    
    return "COMPLETE"

if __name__ =='__main__':
    app.run(host='0.0.0.0')
