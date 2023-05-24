from flask import Blueprint, request
# Blueprint: 라우트를 모아서 관리할 수 있게 해주는 클래스
# request: 클라이언트가 보낸 요청을 확인할 수 있는 클래스

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# 다른 파일에 있는 클래스를 import하기 위해 경로 설정

from service.user_service_imp import User_Service_Imp
from service.email_service_imp import Email_Service_Imp
from service.json_service_imp import Json_Service_Imp
from service.token_service_imp import Token_Service_Imp

from models.schemas import UserSchema

user = Blueprint('user', __name__)  # Blueprint를 이용하면 controller처럼 사용할 수 있다. 

user_schema = UserSchema()
user_service = User_Service_Imp()
json_service = Json_Service_Imp()
token_service = Token_Service_Imp()

@user.route('/login', methods=['POST']) #post 방식만 잡아서 처리한다.
def login():    # 로그인
    jsonData = request.get_json()   # 클라이언트가 보낸 json 데이터를 받아온다.
    return user_service.login(jsonData["uid"], jsonData["upw"]) # 받아온 데이터에서 uid와 upw를 추출하여 login 함수에 넣고 결과값 반환

@user.route("/easylogin", methods=['POST'])
def easylogin():
    jsonData = request.get_json()
    user = user_schema.load(jsonData, partial=True) # 받아온 데이터를 user 형태로 자동 매핑
    return user_service.easylogin(user)


@user.route('/tokenlogin', methods=['POST']) #post 방식만 잡아서 처리한다.
def token_login():    # 토큰 로그인
    jsonData = request.get_json()   # 클라이언트가 보낸 json 데이터를 받아온다.
    return user_service.token_login(jsonData['token']) # 받아온 데이터에서 token을 추출하여 token_login 함수에 넣고 결과값 반환


@user.route('/register', methods=['POST']) #post 방식만 잡아서 처리한다.
def register(): # 회원가입
    jsonData = request.get_json()
    user = user_schema.load(jsonData, partial=True) # 받아온 데이터를 user 형태로 자동 매핑
    return user_service.update(user)


@user.route('/withdrawal', methods=['POST']) #post 방식만 잡아서 처리한다.
def withdrawal():   # 회원탈퇴
    jsonData = request.get_json()
    print(jsonData['token'])
    return user_service.withdrawal(jsonData['token'])


@user.route('/update', methods=['POST']) #post 방식만 잡아서 처리한다.
def user_update():   # 회원정보 수정
    jsonData = request.get_json()
    user = user_schema.load(jsonData, partial=True)
    print(user.profile)
    if json_service.json_key_check(jsonData, "image"):  # 이미지가 있을 경우
        user.profile = user_service.image_upload(jsonData["image"]) # 이미지 업로드
        print(user.profile)
        user_service.delete_image(user) # 기존 이미지 삭제
    print(user.profile)
    return user_service.update(user) 


@user.route('/idcheck', methods=['POST'])
def id_check(): # 아이디 중복체크
    jsonData = request.get_json() 
    return user_service.overlap_check("uid",jsonData['uid'])


@user.route('/nicknamecheck', methods=['POST'])
def nickname_check(): # 닉네임 중복체크
    jsonData = request.get_json()
    return user_service.overlap_check("nickname",jsonData['nickname']) 


@user.route('/emailcheck', methods=['POST'])
def email_check(): # 이메일 중복체크
    jsonData = request.get_json()
    return user_service.overlap_check("email",jsonData['email'])


@user.route('/sendemail', methods=['POST'])
def send_email(): # 이메일 인증번호 전송
    email_check = Email_Service_Imp()
    jsonData = request.get_json()
    return email_check.send_email(jsonData['email'])


@user.route('/findid', methods=['POST'])
def find_id(): # 아이디 찾기
    jsonData = request.get_json()
    user = user_schema.load(jsonData, partial=True)
    return user_service.find_id(user) 

@user.route('/findpw', methods=['POST'])
def find_pw(): # 비밀번호 찾기
    jsonData = request.get_json()
    user = user_schema.load(jsonData, partial=True)
    return user_service.find_pw(user)


@user.route('/info', methods=['POST'])
def user_info(): # 회원정보 조회
    jsonData = request.get_json()
    print(jsonData['token'])
    user_id = token_service.get_id(jsonData['token'])
    print(user_id.uid)
    return user_service.info(user_id.uid)