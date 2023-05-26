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

@medicine.route('/search', methods=['GET']) #get 방식만 잡아서 처리한다.
def search():
    medicine = Medicine().from_request_args(request)
    return medicine_service.search(medicine)

@medicine.route('/detail', methods=['GET']) 
def detail():
    itemSeq = request.args.get("itemSeq", '')   # 품목기준코드
    return medicine_service.detail(itemSeq)

@medicine.route('/bookmark', methods=['POST'])
def bookmark():
    jsonData = request.get_json()
    bookmark = bookmark_schema.load(jsonData, partial=True)
    usertoken = token_service.get_id(jsonData["token"])
    if usertoken == "false":
        return "false"
    else:
        bookmark.uid = usertoken.uid
        return medicine_service.bookmark(bookmark)
    
@medicine.route('/bookmarkoff', methods=['POST'])
def bookmark_off():
    jsonData = request.get_json()
    bookmark = bookmark_schema.load(jsonData, partial=True)
    usertoken = token_service.get_id(jsonData["token"])
    if usertoken == "false":
        return "false"
    else:
        bookmark.uid = usertoken.uid
        return medicine_service.bookmark_off(bookmark)
    
@medicine.route('/bookmarklist', methods=['POST'])
def bookmark_list():
    jsonData = request.get_json()
    bookmark = bookmark_schema.load(jsonData, partial=True)
    usertoken = token_service.get_id(jsonData["token"])
    if usertoken == "false":
        return "false"
    else:
        bookmark.uid = usertoken.uid
        return medicine_service.bookmark_list(bookmark)
    
@medicine.route('/bookmarkall', methods=['POST'])
def bookmark_all():
    jsonData = request.get_json()
    bookmark = bookmark_schema.load(jsonData, partial=True)
    usertoken = token_service.get_id(jsonData["token"])
    if usertoken == "false":
        return "false"
    else:
        bookmark.uid = usertoken.uid
        return medicine_service.bookmark_all(bookmark)

@medicine.route('/image', methods=['POST'])
def image_upload():
        print("사진 검색 들어옴")
        jsonData = request.get_json()
        front = jsonData["front"]
        back = jsonData["back"]

        front_decoded_image_data = base64.b64decode(front)
        front_image_data = io.BytesIO(front_decoded_image_data)

        back_decoded_image_data = base64.b64decode(back)
        back_image_data = io.BytesIO(back_decoded_image_data)

        pillMain = PillMain()
        result = []
        result = pillMain.main(front_image_data, back_image_data)
        print("controller result : ", result)
        result_json = medicine_service.camera_search(result)
        print("constroller result_json : ", result_json)

        return result_json