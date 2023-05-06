import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from service.barcode_service import Barcode_Service
import secret_key.config as config
import requests

class Barcode_Service_IMP(Barcode_Service):

    def search(self, barcode): # 바코드를 받아서 검색
        # api 호출
        response = requests.get(
            f'http://openapi.foodsafetykorea.go.kr/api/{config.BARCODE_KEY}/C005/json/1/5/BAR_CD={barcode}')
        
        # json 형식으로 반환
        return response.json()["C005"]["row"]