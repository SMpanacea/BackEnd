import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from service.user_service import User_Service
from models import db
from models import User
from flask import jsonify   #json 형태로 데이터를 반환하기 위해 사용


#aws s3 사용을 위한 모듈
import boto3   
from botocore.exceptions import ClientError 

# 키 값들을 가져오기 위해 사용
import secret_key.config as config

#이메일 인증을 위한 모듈
from flask_mail import Mail, Message
# 이메일 템플릿을 위한 모듈
from flask import render_template


class User_ServiceImp(User_Service):

    def login(self, uid, upw):  #로그인 함수
        
        try:
            # 아이디와 비밀번호가 일치한 값의 검색 결과가 나오는지 확인
            # result = db.session.query(User).filter(User.uid == uid, User.upw == upw).all() 와 같음
            result = db.session.query(User).filter_by(uid = uid, upw = upw).all()
            
        except Exception as e:
            print(e)
            return 'false'
        else:
            if  result: # 결과값이 존재한다면 로그인 성공
                #사용자의 정보 반환(객체를 json으로 변환하여 반환 - 객체상태로는 반환 불가)
                return jsonify(db.session.query(User).filter_by(uid = uid, upw = upw).first().serialize())
            else :   # 결과값이 존재하지 않는다면 로그인 실패
                return "false"

    

    def logout(self):
        return 'logout'


    def register(self, uid, upw, email, nickname, gender, birth): #회원가입 함수

        try:  #try catch문을 사용하여 데이터 저장

            user = User(
                uid = uid,
                upw = upw,
                email = email,
                nickname = nickname,
                gender = gender,
                birth = birth
            )

            #데이터 저장
            db.session.add(user)
            #데이터 커밋
            db.session.commit()

        except Exception as e:
            print(e)
            return 'false'  # 데이터 저장이 실패한 경우 false 반환
        else:
            return 'true'  #데이터 저장이 성공한 경우 true 반환
        
    def overlap_check(self, key, value):    #중복체크 함수
        print("key:" + key + "  value: " + value)
        try:
            result = db.session.query(User).filter_by(**{key: value}).all()
        except Exception as e:
            print(e)
            return 'false'
        else:
            if result: #결과값이 존재한다면 중복된 값이 존재
                return 'false'
            else:   #결과값이 존재하지 않는다면 중복된 값이 존재하지 않음
                return 'true'
            

    def withdrawal(self, uid):  #회원탈퇴 함수
        try:
            db.session.query(User).filter_by(uid = uid).delete()
            db.session.commit()
        except Exception as e:
            print(e)
            return 'false'
        else:
            return 'true'
        

    def send_email(self, email):    #이메일 인증번호 전송 함수
        from app import mail    #app.py에서 생성한 mail 객체를 가져옴
        import random   #랜덤한 문자열을 생성하기 위해 사용
        import string   

        #랜덤한 문자열 생성
        random_num = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
        # Message() 함수는 이메일의 제목과 송신자, 수신자 등의 정보를 입력받아 이메일을 구성
        msg = Message('Panacea인증번호입니다', sender=config.MAIL_USERNAME, recipients=[email])
        # 이메일의 내용을 html 형식으로 작성 (email.html 파일 에 인증번호 넘겨줌)
        msg.html = render_template('email.html', num = random_num)
        # 메일 전송
        mail.send(msg)
        # 인증번호 반환
        return random_num