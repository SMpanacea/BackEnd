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

    # 바코드 식품 검색 결과 받아오기
    barcode_result = barcode_service.search(barcode_num)

    # 바코드 식품 검색 결과가 없을 경우 
    if barcode_result == 'false':
        # 바코드 의약품 크롤링 검색 결과 반환
        return barcode_service.crawling_search(barcode_num)
    else:
        # 바코드 식품 검색 결과 반환
        return barcode_result


