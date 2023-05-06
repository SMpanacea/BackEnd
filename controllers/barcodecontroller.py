from flask import Blueprint, request

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


from service.barcode_service_imp import Barcode_Service_IMP

barcode = Blueprint('barcode', __name__)


@barcode.route('/search', methods=['GET'])
def search():
    barcode_service = Barcode_Service_IMP()
    # 바코드를 받아서 검색
    barcode_num = request.args.get("barcode", '')
    return barcode_service.search(barcode_num)


