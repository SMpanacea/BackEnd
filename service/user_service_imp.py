import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from service.user_service import User_Service
from models import db
from models import User
from flask import jsonify

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