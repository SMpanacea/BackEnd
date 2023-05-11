from flask import Blueprint, request

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# 다른 파일에 있는 클래스를 import하기 위해 경로 설정

from service.medicine_service_imp import Medicine_Service_Imp

from models.schemas import Medicine
from models.schemas import BookMark


medicine = Blueprint('medicine', __name__)  # Blueprint를 이용하면 controller처럼 사용할 수 있다. 

medicine_service = Medicine_Service_Imp()
bookmark_schema = BookMark()

@medicine.route('/search', methods=['GET']) #get 방식만 잡아서 처리한다.
def search():
    medicine = Medicine().from_request_args(request)
    return medicine_service.search(medicine)

@medicine.route('/detail', methods=['GET']) 
def detail():
    itemSeq = request.args.get("itemSeq", '')   # 품목기준코드
    return medicine_service.detail(itemSeq)

