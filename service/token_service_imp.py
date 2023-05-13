import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from service.token_service import Token_Service
import secret_key.config as config
from models.schemas import UserToken

#토큰 생성을 위한 모듈
from datetime import datetime as dt, timedelta
import jwt


class Token_Service_Imp(Token_Service):
    def generate_token(self, user_id):
        payload = {
            'user_id': user_id,
            'exp': dt.utcnow() + timedelta(days=7),  # 토큰의 유효기간
            'iat': dt.utcnow(),  # 토큰 발행 시간
        }
        secret_key = config.TOKEN_KEY 
        token = jwt.encode(payload, secret_key, algorithm='HS256')  # 토큰 생성
        return token


    def validate_token(self, token):
        secret_key = config.TOKEN_KEY 
        try:
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            return payload.get('user_id')
        except jwt.ExpiredSignatureError:
            # 토큰이 만료된 경우
            return self.generate_token(payload.get('user_id'))   # 토큰 재발행
        except jwt.InvalidSignatureError:
            # 서명이 잘못된 경우
            return "false"
        except Exception as e:
            # 그 외 에러
            print(e)
            return "false"
        

    def get_id(self, token):    # 토큰에서 아이디를 가져오는 함수
        try:
            user_data = self.validate_token(token)
            if user_data.length > 15:    # 토큰이 넘어온 경우
                usertoken = UserToken(id=self.validate_token(user_data), token=user_data)
                return usertoken
            elif user_data == "false":   # 토큰이 잘못된 경우
                return "false"
            else:   # 아이디가 넘어온 경우
                usertoken = UserToken(id=self.validate_token(user_data))
                return usertoken
        except Exception as e:
            print(e)
            return "false"

            
            