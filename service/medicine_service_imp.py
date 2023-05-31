import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
from service.medicine_service import Medicine_Service
from service.json_service_imp import Json_Service_Imp
import secret_key.config as config
import requests
from models.schemas import Medicine, Multi_Info
from models.models import db, BookMark
from flask import jsonify 
import re

class Medicine_Service_Imp(Medicine_Service):

    def search(self, medicine):  # 약 정보 통신 함수
        response = requests.get(config.url, params=medicine.get_params())
        print(response.json())
        return response.json()["body"]  # 약 정보만 반환


    def detail(self, itemSeq):
        search_result = self.search(Medicine(itemSeq=itemSeq))
        multi_result = self.multi_info(itemSeq)
        json_service = Json_Service_Imp()
        if json_service.json_key_check(multi_result["body"], "items"): # 병용 금기 정보가 있을 경우
            detail_result = (self.remove_tags(search_result["items"][0])
                            + self.remove_tags(multi_result["body"]["items"]))
        else:   # 병용 금기 정보가 없을 경우
            detail_result = self.remove_tags(search_result["items"][0])
        return detail_result    # 정보 반환


    def multi_info(self, itemSeq): # 병용 금기 정보 통신 함수
        response = requests.get(config.multi_url, params=Multi_Info(itemSeq=itemSeq).get_params())
        return response.json()
    

    def bookmark(self, bookmark):   # 즐겨찾기 함수
        try:
            db.session.add(bookmark)    # 즐겨찾기 추가
            db.session.commit() # 커밋
        except Exception as e:
            print(e)
            return 'false'
        else:
            return self.bookmark_list(bookmark) # 즐겨찾기 리스트 반환


    def bookmark_off(self, bookmark):   # 즐겨찾기 해제 함수
        try:
            BookMark.query.filter_by(uid=bookmark.uid , itemSeq=bookmark.itemSeq).delete()  # 즐겨찾기 삭제
            db.session.commit() # 커밋
        except Exception as e:
            print(e)
            return 'false'
        else:
            return self.bookmark_list(bookmark) # 즐겨찾기 리스트 반환
        

    def bookmark_list(self, bookmark):   # 즐겨찾기 리스트 함수
        try:
            result = BookMark.query.filter_by(uid=bookmark.uid).all()   # 회원의 즐겨찾기 리스트 가져오기
        except Exception as e:
            print(e)
            return 'false'
        else:
            list = []
            for bookmark_one in result: # 즐겨찾기 리스트를 객체에서 리스트로 변환
                list.append(bookmark_one.__dict__["itemSeq"])
            return jsonify(list)    # 즐겨찾기 리스트 json으로 반환
        

    def bookmark_all(self, bookmark):   # 즐겨찾기 상세 리스트 함수
        try:
            result = BookMark.query.filter_by(uid=bookmark.uid).all()   # 회원의 즐겨찾기 리스트 가져오기
        except Exception as e:
            print(e)
            return 'false'
        else:
            booklist = []
            print(result)
            for bookmark_one in result: # 즐겨찾기 리스트를 객체에서 리스트로 변환
                booklist.append(bookmark_one.serialize())
            print(booklist)
            print([bookmark.serialize() for bookmark in result])
            return  booklist    # 즐겨찾기 상세 리스트  반환
    

    def camera_search(self, list):  # 카메라 검색 함수
        result = []
        for item in list:   # 카메라 검색 리스트를 통해 약 정보 가져오기
            medicine = Medicine(itemSeq=item["code"], numOfRows=1)
            response = requests.get(config.url, params=medicine.get_params())
            result.append(response.json()["body"])
        print("result : ", result)
        return result   # 약 정보 반환
    
    def remove_tags(self, data):
        # HTML 태그를 제거하는 정규식 패턴
        cleanr = re.compile('<.*?>')
        # 정규식 패턴에 매칭되는 모든 문자열을 빈 문자열로 치환
        for key in data:
            if data[key] is None:
                continue
            data[key] = re.sub(cleanr, '', data[key])
        return data







    