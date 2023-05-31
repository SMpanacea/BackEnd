from flask import Blueprint, request

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# 다른 파일에 있는 클래스를 import하기 위해 경로 설정

from service.medicine_service_imp import Medicine_Service_Imp

from models.schemas import Medicine
from models.schemas import BookMarkSchema

# from aimodel.PillMain import PillMain

from service.token_service_imp import Token_Service_Imp

from service.json_service_imp import Json_Service_Imp



import boto3   
from botocore.exceptions import ClientError 
# 키 값들을 가져오기 위해 사용
import secret_key.config as config

import datetime
import time

import io
import base64
from PIL import Image
import json
from aimodel.PillMain import PillMain





medicine = Blueprint('medicine', __name__)  # Blueprint를 이용하면 controller처럼 사용할 수 있다. 

medicine_service = Medicine_Service_Imp()
bookmark_schema = BookMarkSchema()
token_service = Token_Service_Imp()

#검색
@medicine.route('/search', methods=['GET']) #get 방식만 잡아서 처리한다.
def search():
    medicine = Medicine().from_request_args(request)
    # 검색 결과 반환
    return medicine_service.search(medicine)

#세부 내용 
@medicine.route('/detail', methods=['GET']) 
def detail():
    itemSeq = request.args.get("itemSeq", '')   # 품목기준코드
    # 코드에 맞는 세부 내용 반환
    return medicine_service.detail(itemSeq)

#즐겨찾기 추가
@medicine.route('/bookmark', methods=['POST'])
def bookmark():
    jsonData = request.get_json()
    bookmark = bookmark_schema.load(jsonData, partial=True)
    # 토큰에 있는 아이디 가져오기
    usertoken = token_service.get_id(jsonData["token"])
    # 토큰이 잘못된 경우
    if usertoken == "false":
        return "false"
    else: # 토큰이 정상적인 경우
        bookmark.uid = usertoken.uid
        # 회원 아이디에 즐겨찾기 추가
        return medicine_service.bookmark(bookmark)
    
# 즐겨찾기 해제
@medicine.route('/bookmarkoff', methods=['POST'])
def bookmark_off():
    jsonData = request.get_json()
    bookmark = bookmark_schema.load(jsonData, partial=True)
    # 토큰에 있는 아이디값 가져오기
    usertoken = token_service.get_id(jsonData["token"])
    # 토큰이 잘못된 경우
    if usertoken == "false":
        return "false"
    else: #토큰이 정상적인 경우
        bookmark.uid = usertoken.uid
        # 회원 아이디에 즐겨찾기 해제
        return medicine_service.bookmark_off(bookmark)
    
# 즐겨찾기 리스트
@medicine.route('/bookmarklist', methods=['POST'])
def bookmark_list():
    jsonData = request.get_json()
    bookmark = bookmark_schema.load(jsonData, partial=True)
    # 토큰에 있는 아이디값 가져오기
    usertoken = token_service.get_id(jsonData["token"])
    # 토큰이 잘못된 경우
    if usertoken == "false":
        return "false"
    else: # 토큰이 정상적인 경우
        bookmark.uid = usertoken.uid
        # 회원 아이디에 즐겨찾기 리스트 반환
        return medicine_service.bookmark_list(bookmark)
    
# 즐겨찾기 리스트의 전체 내용 
@medicine.route('/bookmarkall', methods=['POST'])
def bookmark_all():
    jsonData = request.get_json()
    bookmark = bookmark_schema.load(jsonData, partial=True)
    # 토큰에 있는 아이디값 가져오기
    usertoken = token_service.get_id(jsonData["token"])
    # 토큰이 잘못된 경우
    if usertoken == "false":
        return "false"
    else:
        bookmark.uid = usertoken.uid
        # 회원 아이디에 즐겨찾기 리스트의 전체 내용 반환
        return medicine_service.bookmark_all(bookmark)

# 이미지로 알역 검색
@medicine.route('/image', methods=['POST'])
def image_upload():
        try:
            print("사진 검색 들어옴")
            jsonData = request.get_json()
            # 알약의 앞면과 뒷면을 받아옴
            front = jsonData["front"]
            back = jsonData["back"]

            front_decoded_image_data = base64.b64decode(front)
            front_image_data = io.BytesIO(front_decoded_image_data)

            back_decoded_image_data = base64.b64decode(back)
            back_image_data = io.BytesIO(back_decoded_image_data)

            pillMain = PillMain()
            result = []
            # 약의 정보를 받아옴 (약의 코드만 리스트로 저장된 상황)
            result = pillMain.main(front_image_data, back_image_data)
            print("controller result : ", result)
            # 약의 세부 정보들 까지 받아옴 (약 하나하나의 세부 정보를 가져온 상황)
            result_json = medicine_service.camera_search(result)
            print("constroller result_json : ", result_json)
            # 약 정보 반환
            return result_json
        except Exception as e:
            print(e)
            return "false"



@medicine.route('/imageFix', methods=['POST'])
def image_fix():
        import requests
        try:
            print("고정 사진 검색 들어옴")
            
            front_url = "https://panacea.s3.ap-northeast-2.amazonaws.com/fix/front.png"
            back_url = "https://panacea.s3.ap-northeast-2.amazonaws.com/fix/back.png"

            front_image_data = io.BytesIO(requests.get(front_url).content)
            back_image_data = io.BytesIO(requests.get(back_url).content)

            pillMain = PillMain()
            result = []
            result = pillMain.main(front_image_data, back_image_data)
            print("controller result : ", result)
            result_json = medicine_service.camera_search(result)
            print("constroller result_json : ", result_json)

            return result_json
        except Exception as e:
            print(e)
            return "false"