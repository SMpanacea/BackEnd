import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from service.barcode_service import Barcode_Service
from service.json_service_imp import Json_Service_Imp
import secret_key.config as config
import requests

class Barcode_Service_IMP(Barcode_Service):

    def search(self, barcode): # 바코드를 받아서 검색
        # api 호출
        response = requests.get(
            f'http://openapi.foodsafetykorea.go.kr/api/{config.BARCODE_KEY}/C005/json/1/5/BAR_CD={barcode}')
        
        if Json_Service_Imp.json_key_check(response.json()["C005"], "row"):
            # 바코드 정보가 존재할 경우
            return response.json()["C005"]["row"]
        else:
            # 바코드 정보가 존재하지 않을 경우
            return "false"