from flask import Blueprint, request
# Blueprint: 라우트를 모아서 관리할 수 있게 해주는 클래스
# request: 클라이언트가 보낸 요청을 확인할 수 있는 클래스

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# 다른 파일에 있는 클래스를 import하기 위해 경로 설정

from service.user_service_imp import User_ServiceImp
# user_service_imp.py에 있는 User_ServiceImp 클래스를 import

user = Blueprint('user', __name__)  # Blueprint를 이용하면 controller처럼 사용할 수 있다. 

@user.route('/login', methods=['POST']) #post 방식만 잡아서 처리한다.
def login():    # 로그인
    user_service = User_ServiceImp()
    jsonData = request.get_json()   # 클라이언트가 보낸 json 데이터를 받아온다.
    return user_service.login(jsonData['uid'], jsonData['upw']) # 받아온 데이터에서 uid와 upw를 추출하여 login 함수에 넣고 결과값 반환


@user.route('/register', methods=['POST']) #post 방식만 잡아서 처리한다.
def register(): # 회원가입
    user_service = User_ServiceImp()
    jsonData = request.get_json()
    return user_service.register(jsonData['uid'], 
                                jsonData['upw'],
                                jsonData['email'],
                                jsonData['nickname'],
                                jsonData['gender'],
                                jsonData['birth'])

@user.route('/withdrawal', methods=['POST']) #post 방식만 잡아서 처리한다.
def withdrawal():   # 회원탈퇴
    user_service = User_ServiceImp()
    jsonData = request.get_json()
    return user_service.withdrawal(jsonData['uid'])


@user.route('/userupdate', methods=['POST']) #post 방식만 잡아서 처리한다.
def user_update():   # 회원정보 수정
    user_service = User_ServiceImp()
    jsonData = request.get_json()
    return user_service.update(jsonData['uid'],
                                    jsonData['upw'],
                                    jsonData['email'],
                                    jsonData['nickname'],
                                    jsonData['gender'],
                                    jsonData['birth'])

@user.route('/idcheck', methods=['POST'])
def id_check(): # 아이디 중복체크
    user_service = User_ServiceImp()
    jsonData = request.get_json() 
    return user_service.overlap_check("uid",jsonData['uid'])


@user.route('/nicknamecheck', methods=['POST'])
def nickname_check(): # 닉네임 중복체크
    user_service = User_ServiceImp()
    jsonData = request.get_json()
    return user_service.overlap_check("nickname",jsonData['nickname']) 


@user.route('/emailcheck', methods=['POST'])
def email_check(): # 이메일 중복체크
    user_service = User_ServiceImp()
    jsonData = request.get_json()
    return user_service.overlap_check("email",jsonData['email'])


@user.route('/sendemail', methods=['POST'])
def send_email(): # 이메일 인증번호 전송
    user_service = User_ServiceImp()
    jsonData = request.get_json()
    return user_service.send_email(jsonData['email'])