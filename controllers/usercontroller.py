from flask import Blueprint, request

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# 다른 파일에 있는 클래스를 import하기 위해 경로 설정

from service.user_service_imp import User_ServiceImp

user = Blueprint('user', __name__)  # Blueprint를 이용하면 controller처럼 사용할 수 있다. 

@user.route('/login', methods=['POST']) #post 방식만 잡아서 처리한다.
def login():
    user_service = User_ServiceImp()
    jsonData = request.get_json()
    return user_service.login(jsonData['uid'], jsonData['upw'])

@user.route('/register', methods=['POST']) #post 방식만 잡아서 처리한다.
def register():
    user_service = User_ServiceImp()
    jsonData = request.get_json()
    return user_service.register(jsonData['uid'], 
                                 jsonData['upw'],
                                 jsonData['email'],
                                 jsonData['nickname'],
                                 jsonData['gender'],
                                 jsonData['birth'])