
import numpy as np
import fasttext
from PyKomoran import *
import re
from random import randint

komoran=Komoran("EXP")
model=fasttext.load_model("model_0602.bin")

#코사인 유사도
def similarity(v1,v2):
    n1=np.linalg.norm(v1)
    n2=np.linalg.norm(v2)
    simy=np.dot(v1,v2)/n1/n2
    if simy>1:
        return 1.0
    elif simy<0:
        return 0.0
    else:
        return simy

#유사한 단어 리스트 생성
#fa_model = 신경망 모델
#sentence = 유저가 입력한 문장 전처리한 다차원 리스트([n][0]:형태소,[n][1]:품사)
#pre_vocab = 감정 키워드 리스트
def findmaxsim(input_type, fa_model, sentence, pre_vocab):
    diary=[] #diary 리스트 선언
    for i in range(len(sentence)):
        diary.append(sentence[i][0]) #diary리스트에 형태소만 넣어준다.
        
    sim_list=list()#유사도가 최대로 나온 키워드들 넣어줄 리스트 선언
    for i in range(len(diary)):
        max=0
        
        for j in range(len(pre_vocab)):
            #한 형태소 별로 모든 감정 키워드와 유사도 측정하기 위해서 이중포문
            #similarity(형태소, 키워드) : 형태소와 키워드 유사도 측정
            temp=similarity(fa_model.get_word_vector(diary[i]),fa_model.get_word_vector(pre_vocab[j]))
            if temp>max:
                max=temp
                word=pre_vocab[j]
        if input_type == 'plan':
            sim_list.append((word, max))
        
        else:
            #해당 형태소가 명사라면 유사도가 0.4이상인 경우에만 sim_list에 넣어줌.
            #명사일 때 유사도 max값 0.4 안넘으면 해당 키워드는 감정분석에 사용 안함
            if(sentence[i][1] == 'NNG' or sentence[i][1] == 'NNP' or sentence[i][1] == 'NA' or sentence[i][1] == 'XR'):
                if(max >0.4):
                    sim_list.append((word,max))
            #명사 아니면 유사도와 상관없이 sim_list에 추가시켜준다.
            else:
                sim_list.append((word, max))
    #print('유사도 전체', sim_list)        
    return sim_list
    
    



#전처리
#인자로 들어오는 diary: 유저 입력 문장 전처리 시키기 위해 호출할 때는 str타입
#                     : 최종 결과 리스트 만들기 위해 호출할 때는 list타입-감정 분석에 사용 한 키워드들 리스트
def preprocessing(input_type, diary):
        
    #유저 입력 문장 전처리할 때 실행되는 코드
    if input_type == 'diary':        
        diary=komoran.get_plain_text(diary)
        #print('전처리함수 문장 전처리:', diary)
        morp_list = []
        morp_list = diary.split(' ')

        final_list = []
        for i in range(len(morp_list)):
            #print(morp_list[i])
            token = morp_list[i].split('/')
            #print('스플릿한 토큰: ', token)
            #print('token타입', type(token))
            if token[0] == morp_list[i]:
                token = [morp_list[i], 'NA']
                #print('스플릿한 토큰2: ', token)
            final_list.append(token)
        #print('line67 전처리함수 final_list', final_list)
        emotion = []
    

        for i in range(len(final_list)):
            if(final_list [i][1] == 'NA' or final_list[i][1] == 'MAG' or final_list[i][1]=='VA' or final_list[i][1]=='XR' or final_list[i][1]=='NNG' or final_list[i][1]=='VV' or final_list[i][1]=='NNP'):
                if final_list[i][0] != '오늘':
                    if(len(final_list[i][0])>0):
                        if final_list[i][1] == 'VV':
                            if final_list[i][0]=='하' or final_list[i][0]=='오' or final_list[i][0]=='가':
                                continue
                        emotion.append((final_list[i][0], final_list[i][1]))
        #print(emotion)
        return emotion
    else:
        diary=komoran.get_plain_text(diary)
        morp_list = []
        morp_list = diary.split(' ')

        final_list = []
        for i in range(len(morp_list)):
            #print(morp_list[i])
            token = morp_list[i].split('/')
            #print('스플릿한 토큰: ', token)
            #print('token타입', type(token))
            if token[0] == morp_list[i]:
                token = [morp_list[i], 'NA']
                #print('스플릿한 토큰2: ', token)
            final_list.append(token)
        #print('line67 전처리함수 final_list', final_list)
        
        plan = []
    

        for i in range(len(final_list)):
            if(final_list [i][1] == 'NA' or final_list[i][1]=='XR' or final_list[i][1]=='NNG' or final_list[i][1]=='NNP'):
                if(len(final_list[i][0])>0):
                    plan.append((final_list[i][0], final_list[i][1]))
        #print(plan)
        return plan
        


#감정 정도 계산
def pointwithweight(res_dict,cnt_dict, dict_sim):
    emo_deg = [0, 0, 0, 0, 0]
    emo_sum = 0
    for word in cnt_dict:       
        if res_dict[word]== -5:
            emo_deg[0] += (cnt_dict[word]*dict_sim[word])
        elif res_dict[word]== -3:
            emo_deg[1] += (cnt_dict[word]*dict_sim[word])
        elif res_dict[word]== 1:
            emo_deg[2] += (cnt_dict[word]*dict_sim[word])
        elif res_dict[word]== 3:
            emo_deg[3] += (cnt_dict[word]*dict_sim[word])
        else:
            emo_deg[4] += (cnt_dict[word]*dict_sim[word])
            
    for i in range(len(emo_deg)):
        emo_sum += emo_deg[i]
        
    for i in range(len(emo_deg)):
        emo_deg[i] = 100.0*(emo_deg[i]/emo_sum)
        
    #print(emo_deg)
    return emo_deg
            
    



#몇 번 나왔는지 계산(튜플 형태라 .count 메소드 사용 불가한 경우)
def countw(slist, word):
    cnt=0
    for i in range(len(slist)):
        if wd(slist[i])==word:
            cnt=cnt+1
    return cnt

#튜플의 두 번째 인자
def sim(t):
    return t[1]

#튜플의 첫 번째 인자
def wd(t):
    return t[0]

#해당 단어가 가지는 가장 높은 유사도
def maxsim(slist,word):
        for i in range(len(slist)):
            if wd(slist[i])==word:
                return sim(slist[i])#유사도 기준으로 정렬했으니까 제일 앞에 나오는게 max값

#0.5 이상인 경우만 집계
def morethanhalf(slist):
    t_list=list()
    for i in range(len(slist)):
        if sim(slist[i])>=0.5:
            t_list.append(slist[i])
        else:
            return t_list#유사도 기준으로 정렬했으니까 한번 0.5 미만이라면 그 뒤도 계속 0.5 미만

#일기->감정
def feeling(diary,fa_model):

    

    #리스트-감정  
    fllist=['화나', '참담', '배신', '증오', '서럽', '분노', '공포', '무섭', '겁', '미워', '미움', '미워하', '흑역사', '짜증',
            '어이없', '화', '지랄', '찝찝하다', '찝찝', '싸우', '싸움', '망', '아쉽', '눈물', '지루', '지치', '지침', '혼란', '당황', '의심', '외롭', '외로움', '슬프', '슬픔', '성가시', '성가심', '서운', '부끄럽', '수치', '수치심', '부끄러움', '곤란', '허탈', '허전', '속상하', '속상', '더럽', '복잡', '미안', '후회', '아파서', '아프', '어쩌',
           '비밀', '존경', '평화', '차분', '진정', '온순', '조용', '확고', '장난', '이성', '평온', '마지막', '위로', '기대',
           '응원','성공', '잘', '해결', '이쁘', '예쁘', '매력', '자랑', '통쾌', '낙관', '유머', '재치', '우정', '감사', '재밌', '고맙', '좋', '좋아서', '설레', '유쾌', '시원', '홀가분', '유머러스', '공손', '귀여움', '귀여워', '날라가', '날아가', '웃기', '반하', '맛있', '멋지', '멋있', '따뜻', '쏠쏠',
           '행복', '사랑', '입맞춤', '애정', '즐겁', '활기차', '신나', '미치', '황홀', '발랄', '쾌활', '존예', '존잼', '존맛', '좋아하', '최고']

    #딕셔너리-감정
    fldict={#아주 나쁨-(분노/절망/짜증)
    '화나':-5, '참담':-5, '배신':-5, '증오':-5, '서럽':-5, '분노':-5, '공포':-5, '겁':-5, '미워':-5, '미움':-5, '미워하':-5, '흑역사':-5, '짜증':-5,

    #나쁨-(불안/슬픔/걱정)
    '어이없':-3, '화':-3, '지랄':-3, '찝찝하다':-3, '찝찝':-3, '싸우':-3, '싸움':-3,'무섭':-3,  '망':-3, '아쉽':-3, '눈물':-3, '지루':-3, '지치':-3, '지침':-3, '혼란':-3, '당황':-3, '의심':-3, '외롭':-3, '외로움':-3, '슬프':-3, '슬픔':-3, '성가시':-3, '성가심':-3, '서운':-3, '부끄럽':-3, '수치':-3, '수치심':-3, '부끄러움':-3, '곤란':-3, '허탈':-3, '허전':-3, '속상하':-3, '속상':-3, '더럽':-3, '복잡':-3, '미안':-3, '후회':-3, '아파서':-3, '아프':-3, '어쩌':-3,

    #보통-(평온/관심/수용)
    '비밀':1, '존경':1, '평화':1, '차분':1, '진정':1, '온순':1, '조용':1, '확고':1, '괜찮':1, '장난':1, '이성':1, '평온':1, '마지막':1, '위로':1, '기대':1,

    #좋음-(기쁨/ 낙천/ 기대)
    '응원':3, '성공':3, '잘':3, '해결':3, '이쁘':3, '예쁘':3, '매력':3, '자랑':3, '통쾌':3, '낙관':3, '유머':3, '재치':3, '우정':3, '감사':3, '재밌':3, '고맙':3,'좋':3, '좋아서':3, '설레':3, '유쾌':3, '시원':3, '홀가분':3, '유머러스':3, '공손':3, '귀여움':3, '귀여워':3, '날라가':3, '날아가':3, '웃기':3, '반하':3, '맛있':3, '멋지':3, '멋있':3, '따뜻':3, '쏠쏠':3,

    #아주 좋음-(사랑/황홀/즐거움)
    '행복':5, '사랑':5, '입맞춤':5, '애정':5, '즐겁':5, '활기차':5, '신나':5, '미치':5, '황홀':5, '발랄':5, '졸귀':5, '쾌활':5, '존예':5, '존잼':5, '존맛':5, '좋아하':5,  '최고':5}#감정-정도


    resfl=['분노/절망/짜증','불안/슬픔/걱정','평온/관심/수용','기쁨/ 낙천/ 기대','사랑/황홀/즐거움']


    #스트링 전처리: (띄어쓰기->)형태소
    sentence=preprocessing('diary', diary)
    #print('line 181 sentence전처리: ',sentence)
    #print()
    if len(sentence)==0:
        return 'ERROR'

    #유사도 비교 및 결과 저장
    simlist=findmaxsim('diary', fa_model, sentence,fllist)
    #print('line187 키워드별 유사도:',simlist)
    if len(simlist)==0:
        return 'ERROR'

    
    simlist.sort(key=sim,reverse=True)
    finlist=simlist#[:(int)(len(simlist)/2)]


    #print()
    
    result_list=list()
    for i in range(len(finlist)):
        result_list.append(finlist[i][0])
     
    last_keyword_list = result_list

    dict_fin=dict()
    cnt=0
    #count해서 dictionary 생성
    for i in range(len(fllist)):
        if result_list.count(fllist[i])!=0:
            dict_fin[fllist[i]]=result_list.count(fllist[i])
            cnt += result_list.count(fllist[i])

            

    
    #각 키워드별 유사도 합
    dict_sim = dict()
    for i in range(len(fllist)):
        if result_list.count(fllist[i])!=0:
            dict_sim[fllist[i]]=0

    for i in range(len(dict_sim)):
        for j in range(cnt):
            dict_sim[finlist[j][0]] += finlist[j][1]



    respoint = []
    #pointweight
    respoint=pointwithweight(fldict,dict_fin, dict_sim)
    emo={}
    for obj in range(len(respoint)):
        if obj == 0:
            emo['분노/절망/짜증']=(round(respoint[obj],1))

        elif obj == 1:
            emo['불안/슬픔/걱정']=(round(respoint[obj],1))

        elif obj == 2:
            emo['평온/관심/수용']=(round(respoint[obj],1))

        elif obj == 3:
            emo['기쁨/낙천/기대']=(round(respoint[obj],1))

        else:
            emo['사랑/황홀/즐거움']=(round(respoint[obj],1))


    return emo
        
            
    
    
    


#다이어리로 들어갔지만 계획
def planning(diary,fa_model):

    

    pllist=['회의', '면접', '미팅', '회사', '거래처', '발표', '소개팅', '상견례', '병문안', '장례식', '결혼식', '돌잔치', '출장', '수업', '학원', '학교', '컨퍼런스',

'생일', '쇼핑', '카페', '바다', '등산', '맛집', '데이트', '파티', '술집', '클럽', '산책', '운동', '노래방', '축제', '미용', '공원', '공연', '미술관', '영화', '뮤지컬', '연극']
    pldict = {'회의':1, '면접':2, '미팅':1, '회사':1, '거래처':1, '발표':2, '소개팅':2, '상견례':2, '병문안':3, '장례식':4, '결혼식':4, '돌잔치':2, '출장':1, '수업':1, '학원':1, '학교':1, '컨퍼런스':3,

'생일':3, '쇼핑':1, '카페':1, '바다':1, '등산':2, '맛집':1, '데이트':1, '파티':3, '술집':1, '클럽':3, '산책':1, '운동':1, '노래방':2, '축제':3, '미용':1, '공원':1, '공연':1, '미술관':2, '영화':1, '뮤지컬':2, '연극':2}
    
    #스트링 전처리: 띄어쓰기->형태소
    sentence=preprocessing('plan', diary)
    if len(sentence) == 0:
        random_index = randint(0, 37)
        random_keyword = pllist[random_index]
        return random_keyword


    #유사도 비교 및 결과 저장
    simlist=findmaxsim('plan', fa_model,sentence,pllist)
    
    sim_weight_list = []
    for i in range(len(simlist)):
        sim_weight_list.append((simlist[i][0], simlist[i][1]*pldict[simlist[i][0]]))
        
    

    sim_weight_list.sort(key=sim,reverse=True)#유사도 기준으로 내림차순 정렬
    #print('가중치 준 시밀러리스트: ',sim_weight_list)
    '''#만일 제일 높은 유사도가 0.5 이상이라면 0.5 이상만 집계 그렇지 못할 시에는 그냥 전체에서 반 자르기
    if sim(simlist[0])>=0.5:
        finlist=morethanhalf(simlist)
    else:
        finlist=simlist[:(int)(len(simlist)/2)]'''
    finlist= []
    finlist = sim_weight_list
    #여기까지 하면 제일 유사도가 높은 단어들이 전체의 반만큼 만들어짐.

    
    '''set_list=list()
    for i in range(len(finlist)):
        set_list.append(finlist[i][0])
    
    set_list=list(set(set_list))

    if len(set_list)==1:    #한 종류라면 바로 반환
        return set_list[0]



    result_list=list()
    for i in range(len(set_list)):
        result_list.append((set_list[i],countw(finlist,set_list[i]),maxsim(finlist,set_list[i])))
    #위 작업으로 (단어, 카운트, max유사도)를 갖는 리스트 형성


    result_list.sort(key=sim,reverse=True)#key=sim인데 그냥 튜플 두 번째 인자라 실제로는 카운트 기준으로 정렬


    #그다음 제일 첫번째 원소의 카운트랑 비교해서 카운트가 같은 값이 있다면 
    temp_most=result_list[0]


    for i in range(len(result_list)):
        if temp_most[1]==result_list[i][1]:
            if temp_most[2]<result_list[i][2]:
                temp_most=result_list[i] #유사도를 비교한다
        else:
            return wd(temp_most)#카운트가 같은 값이 아니라면 빈도가 더 낮을 것이므로 바로 반환
    '''
    
    return finlist[0][0]


def analyze_diary(content):
    emotion_list=feeling(content,model)
    print(emotion_list)
    return emotion_list

    
def analyze_plan(content):
    keyword=planning(content,model)
    print(keyword)
    return keyword




##실험용
#
#sent = input("[일기 입력]")
#
##이모티콘, 특수문자 제거
#emoji_pattern = re.compile("["
#                             u"\U00010000-\U0010FFFF"
#                             "]+", flags = re.UNICODE)
#han = re.compile(r'[ㄱ-ㅎㅏ-ㅣ!?~,".\n\r#\ufeff\u200d]')    
#
#tokens = re.sub(emoji_pattern, " ", sent)
#tokens = re.sub(han, " ", tokens)
#
#sent = tokens
#
#
#print(feeling(sent,model))
#print()
#print(planning(sent,model))