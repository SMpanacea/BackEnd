import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from service.medicine_service import Medicine_Service
from service.json_service_imp import Json_Service_Imp
import secret_key.config as config
import requests
from models.schemas import Medicine, Multi_Info
from models.models import db, BookMark
from flask import jsonify 

class Medicine_Service_Imp(Medicine_Service):

    def search(self, medicine):  # 약 정보 통신 함수
        response = requests.get(config.url, params=medicine.get_params())
        print (response.json())
        print(medicine.get_params())
        return response.json()["body"]


    def detail(self, itemSeq):
        search_result = self.search(Medicine(itemSeq=itemSeq))
        multi_result = self.multi_info(itemSeq)
        json_service = Json_Service_Imp()
        if json_service.json_key_check(multi_result["body"], "items"): # 병용 금기 정보가 있을 경우
            detail_result = search_result["items"][0] + multi_result["body"]["items"]
        else:   # 병용 금기 정보가 없을 경우
            detail_result = search_result["items"][0]
        return detail_result


    def multi_info(self, itemSeq): # 병용 금기 정보 통신 함수
        response = requests.get(config.multi_url, params=Multi_Info(itemSeq=itemSeq).get_params())
        return response.json()
    

    def bookmark(self, bookmark):   # 즐겨찾기 함수
        try:
            db.session.add(bookmark)
            db.session.commit()
        except Exception as e:
            print(e)
            return 'false'
        else:
            return 'true'

    def bookmark_off(self, bookmark):   # 즐겨찾기 해제 함수
        try:
            BookMark.query.filter_by(uid=bookmark.uid , itemSeq=bookmark.itemSeq).delete()
            db.session.commit()
        except Exception as e:
            print(e)
            return 'false'
        else:
            return 'true'
        
    def bookmark_list(self, bookmark):   # 즐겨찾기 리스트 함수
        try:
            result = BookMark.query.filter_by(uid=bookmark.uid).all()
        except Exception as e:
            print(e)
            return 'false'
        else:
            return jsonify(result)
    








    