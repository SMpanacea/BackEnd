import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from service.user_service import User_Service
import secret_key.config as config
import psycopg2.extras

class User_ServiceImp(User_Service):

    conn = psycopg2.connect(dbname=config.DB_NAME,
                        user=config.DB_USER,
                        password=config.DB_PASS,
                        host=config.DB_HOST)
    #데이터 베이스 연결 설정

    def __init__(self): #생성자
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) #PostgreSQL 연결

    def login(self, id, password):  #로그인 함수
        
        s = "SELECT * FROM users where user_id = '"+id+"' and pass = '"+password+"';"

        try:
            self.cur.execute(s) 
            result = self.cur.fetchone() #결과값 하나를 변수에 저장함
            if  result: # 결과값이 존재한다면 로그인 성공
                return "True" + s
            else :   # 결과값이 존재하지 않는다면 로그인 실패
                return "False" + s
        except Exception as e:
            print(e)
        return 'fail'
    

    def logout(self):
        return 'logout'


    def register(self, uid, upw, email, nickname, gender, birth): #회원가입 함수

        try:  #try catch문을 사용하여 데이터 저장
            self.cur.execute("INSERT INTO users (uid, upw, email, nickname, gender, birth) VALUES (%s, %s, %s, %s, %s, %s)", (uid, upw, email, nickname, gender, birth)) #데이터 저장 
            self.conn.commit() #저장후 db commit
        except Exception as e:
            print(e)
            return 'fail'  # 데이터 저장이 실패한 경우 fail 반환
        return 'success'  #데이터 저장이 성공한 경우 success 반환
            

    def jsontest(): #json 데이터 테스트
        try: 
            # jsonData = request.get_json()
            # print (jsonData['id'])
            # print (jsonData['password'])
            return 'success'
        except Exception as e:
            print(e)
            return 'fail'