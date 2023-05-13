import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from service.user_service import User_Service
from models.models import db
from models.models import User
from flask import jsonify   #json 형태로 데이터를 반환하기 위해 사용

from service.token_service_imp import Token_Service_Imp


#aws s3 사용을 위한 모듈
import boto3   
from botocore.exceptions import ClientError 
# 키 값들을 가져오기 위해 사용
import secret_key.config as config

#토큰 생성을 위한 모듈
from datetime import datetime as dt, timedelta
import jwt

token_service = Token_Service_Imp()

class User_Service_Imp(User_Service):

    def login(self, user):  #로그인 함수
        try:
            # 아이디와 비밀번호가 일치한 값의 검색 결과가 나오는지 확인
            result = User.query.filter_by(uid = user.uid, upw = user.upw).all()
        except Exception as e:
            print(e)
            return 'false'
        else:
            if  result: # 결과값이 존재한다면 로그인 성공
                token = token_service.generate_token(user.uid)   # 토큰 생성
                return token
            else :   # 결과값이 존재하지 않는다면 로그인 실패
                return "false"


    def token_login(self, token):  # 토큰 로그인 함수
        user_data = token_service.validate_token(token)
        if user_data == "false":
            return "false"
        else:   
            return user_data


    def update(self, user): #회원정보 추가 및 수정 함수
        try:  #try catch문을 사용하여 데이터 저장
            #데이터 저장
            db.session.add(user)
            #데이터 커밋
            db.session.commit()
        except Exception as e:
            print(e)
            return 'false'  # 데이터 저장이 실패한 경우 false 반환
        else:
            return 'true'  #데이터 저장이 성공한 경우 true 반환
        
        
    def withdrawal(self, token):  #회원탈퇴 함수
        try:
            usertoken = token_service.get_id(token) #토큰에서 아이디 추출
            if usertoken == "false":    #토큰이 유효하지 않은 경우
                return "false"
            else:   #토큰이 유효한 경우
                User.query.filter_by(uid = usertoken.id).delete()
                db.session.commit()
        except Exception as e:
            print(e)
            return 'false'
        else:
            return 'true'
        

    def overlap_check(self, key, value):    #중복체크 함수
        try:
            result = User.query.filter_by(**{key: value}).all()
        except Exception as e:
            print(e)
            return 'false'
        else:
            if result: #결과값이 존재한다면 중복된 값이 존재
                return 'false'
            else:   #결과값이 존재하지 않는다면 중복된 값이 존재하지 않음
                return 'true'
            
    def find_id(self, user):
        try:
            result = User.query.filter_by(email = user.email).first()
        except Exception as e:
            print(e)
            return 'false'
        else:
            if result:
                return jsonify(result.uid)
            else:
                return 'true'
            
    
    # def info(self, key, value): #회원정보 조회 함수
    #     try:
    #         result = db.session.query(User).filter_by(**{key: value}).all()
    #     except Exception as e:
    #         return 'false'
    #     else:
    #         if result: #결과값이 존재한다면 
    #             return jsonify(result[0].serialize())
    #         else:   #결과값이 존재하지 않는다면 
    #             return 'true'

