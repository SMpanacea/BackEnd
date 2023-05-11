import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from service.user_service import User_Service
from models.models import db
from models.models import User
from flask import jsonify   #json 형태로 데이터를 반환하기 위해 사용


#aws s3 사용을 위한 모듈
import boto3   
from botocore.exceptions import ClientError 
# 키 값들을 가져오기 위해 사용
import secret_key.config as config

#토큰 생성을 위한 모듈
from datetime import datetime as dt, timedelta
import jwt


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
                token = self.generate_token(user.uid)   # 토큰 생성
                json_login = {
                    "login" : "true",
                    "token" : token
                }
                #사용자의 정보 반환(객체를 json으로 변환하여 반환 - 객체상태로는 반환 불가)
                return json_login
            else :   # 결과값이 존재하지 않는다면 로그인 실패
                return "false"
            

    def generate_token(self, user_id):  # 토큰 생성 함수
        payload = {
            'user_id': user_id,
            'exp': dt.utcnow() + timedelta(days=7),  # 토큰의 유효기간
            'iat': dt.utcnow(),  # 토큰 발행 시간
        }
        secret_key = config.TOKEN_KEY 
        token = jwt.encode(payload, secret_key, algorithm='HS256')  # 토큰 생성
        return token

    def token_login(self, token):  # 토큰 로그인 함수
        secret_key = config.TOKEN_KEY 
        try:
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            user_id = payload.get('user_id')
            # 필요한 경우 user_id를 반환
            return user_id
        except jwt.ExpiredSignatureError:
            # 토큰이 만료된 경우
            json_login = {
                    "user_id" : user_id,
                    "token" : self.generate_token(user_id)
                }
            return json_login
        except jwt.InvalidSignatureError:
            # 서명이 잘못된 경우
            return "false"
        except Exception as e:
            # 그 외 에러
            print(e)
            return "false"

    

    def logout(self):
        return 'logout'


    def register(self, user): #회원가입 함수
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
        
        
    def withdrawal(self, user):  #회원탈퇴 함수
        try:
            User.query.filter_by(uid = user.uid).delete()
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

