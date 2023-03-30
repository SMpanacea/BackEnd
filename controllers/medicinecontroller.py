from flask import Blueprint, request

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# 다른 파일에 있는 클래스를 import하기 위해 경로 설정

from service.medicine_service_imp import Medicine_Service_Imp

medicine = Blueprint('medicine', __name__)  # Blueprint를 이용하면 controller처럼 사용할 수 있다. 

@medicine.route('/search', methods=['POST']) #post 방식만 잡아서 처리한다.
def search():
    medicine_service = Medicine_Service_Imp()
    jsonData = request.get_json()
    return medicine_service.search(jsonData['itemSeq'])
