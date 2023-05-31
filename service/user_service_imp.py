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

import datetime
import time

import io
import base64


from sqlalchemy import select, and_


token_service = Token_Service_Imp()

class User_Service_Imp(User_Service):

    def login(self, id, pw):  #로그인 함수
        try:
            print(id, pw)
            # 아이디와 비밀번호가 일치한 값의 검색 결과가 나오는지 확인
            result = User.query.filter_by(uid = id, upw = pw).first()
        except Exception as e:
            print(e)
            return 'false'
        else:
            if  result: # 결과값이 존재한다면 로그인 성공
                token = token_service.generate_token(result.uid)   # 토큰 생성
                return token
            else :   # 결과값이 존재하지 않는다면 로그인 실패
                return "false"
            
    def easylogin(self, user):  #간편 로그인 함수
        user_id = user.uid
        try:
            result = User.query.filter_by(uid = user_id).first()    # 아이디가 일치하는 값의 검색 결과가 나오는지 확인
        except Exception as e:
            print(e)
            return 'false'
        else:
            if result:  # 결과값이 존재
                token = token_service.generate_token(result.uid)    # 토큰 생성
                print("token",token)
                return token    # 토큰 반환
            elif result == None:    # 결과값이 존재하지 않은경우
                self.update(user)   # 회원정보 추가
                token = token_service.generate_token(user_id)   # 토큰 생성
                print("...?",token)
                return token    # 토큰 반환
            else: 
                return 'false'


    def token_login(self, token):  # 토큰 로그인 함수
        user_data = token_service.validate_token(token) # 토큰이 유효한지 확인
        if user_data == "false":    # 토큰이 유효하지 않은 경우
            return "false"
        else:      # 토큰이 유효한 경우
            return 'true'


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
            return self.info(user.uid)  #데이터 저장이 성공한 경우 회원정보 반환
        
        
    def withdrawal(self, token):  #회원탈퇴 함수
        try:
            usertoken = token_service.get_id(token) #토큰에서 아이디 추출
            print("탈퇴",usertoken.uid)
            if usertoken == "false":    #토큰이 유효하지 않은 경우
                print("탈퇴 함수중 토큰이 유효하지 않음")
                return "false"
            else:   #토큰이 유효한 경우
                print("삭제 드가자~")
                User.query.filter_by(uid = usertoken.uid).delete()  #아이디가 일치하는 회원정보 삭제
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
            result = User.query.filter_by(email = user.email).first()   #이메일이 일치하는 값의 검색 결과가 나오는지 확인
        except Exception as e:
            print(e)
            return 'false'
        else:
            if result:  # 결과값이 존재한다면 아이디 반환
                return jsonify(result.uid)
            else:   # 결과값이 존재하지 않는다면 false 반환
                return 'false'
            

    def find_pw(self, user):    #비밀번호 찾기 함수
        try:
            result = User.query.filter_by(uid = user.uid, email = user.email).first()   #아이디와 이메일이 일치하는 값의 검색 결과가 나오는지 확인
        except Exception as e:
            print(e)
            return 'false'
        else:
            if result:
                return "true"   # 결과값이 존재한다면 true 반환 (알려주는게 아닌 바꾸게 해야해서)
            else:
                return 'false'  # 결과값이 존재하지 않는다면 false 반환
            

    def image_upload(self, base64_image_data):
        # S3 서비스를 사용하기 위한 리소스 객체 생성
        s3 = boto3.resource(
            's3',
            aws_access_key_id=config.AWS_ACCESS_KEY,
            aws_secret_access_key=config.AWS_SECRET_KEY,
            region_name=config.AWS_REGION
                            )
        # 현재 날짜를 구합니다.
        now = datetime.datetime.now()
        year_str = now.strftime('%Y')
        month_str = now.strftime('%m')
        day_str = now.strftime('%d')

        # 오늘 날짜에 해당하는 폴더가 없으면 생성합니다.
        bucket = s3.Bucket(config.bucket_name)
        bucket.put_object(Key=f'{year_str}/{month_str}/{day_str}/')

        # 파일이름 지정.
        file_ext = os.path.splitext(base64_image_data[:50])[-1] or '.png'
        filename = 'image_' + str(time.time()) + file_ext


        # S3 객체 이름 지정
        object_name = os.path.splitext(filename)[0] + '_' + str(time.time()) + os.path.splitext(filename)[1]

        # 디코딩된 이미지 데이터를 BytesIO 객체로 변환합니다.
        encoded_image_data = base64_image_data.split(",")[-1]
        decoded_image_data = base64.b64decode(encoded_image_data)
        image_data = io.BytesIO(decoded_image_data)

        # 파일을 S3 버킷에 업로드합니다.
        object_key = f'{year_str}/{month_str}/{day_str}/{object_name}'
        bucket.upload_fileobj(image_data, object_key)

        # 업로드된 객체의 URL을 생성합니다.
        url = bucket.meta.client.generate_presigned_url('get_object', Params={'Bucket': config.bucket_name, 'Key': object_key}, ExpiresIn=3600)
        print(url)

        return url # 파일 업로드된 객체 URI 반환합니다.
    
    def delete_image(self, user):
        # user.profile에 있는 이미지 주소
        image_path = user.profile

        # 이미지 파일 이름 추출 (object_key)
        filename = image_path.split('/')[-1]

        s3 = boto3.resource(
            's3',
            aws_access_key_id=config.AWS_ACCESS_KEY,
            aws_secret_access_key=config.AWS_SECRET_KEY,
            region_name=config.AWS_REGION
            )

        # 지정된 버킷 이름
        bucket_name = config.bucket_name

        try:
            # S3 버킷에서 지정된 파일 삭제
            s3.Object(bucket_name, filename).delete()
            print(f"{filename} Successfully deleted from S3")
        except Exception as e:
            print(f"Error deleting {filename} from S3: {e}")
    
    
    def info(self, uid): #회원정보 조회 함수
        try:
            result = User.query.filter_by(uid = uid).first()
            print("객체임!",result)
            print("그래서 아이디는",result.uid)
        except Exception as e:
            print(e)
            return 'false'
        else:
            if result: #결과값이 존재한다면 
                return result.serialize()
            else:   #결과값이 존재하지 않는다면 
                return 'false'
