import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from service.medicine_service import Medicine_Service
import secret_key.config as config
import requests

class Medicine_Service_Imp(Medicine_Service):

    
    def list(self, pageNo, entpName, itemName, itemSeq, efcyQesitm):
        search_result = self.search(pageNo, entpName, itemName, itemSeq, efcyQesitm)
        return search_result

    def detail(self, itemSeq):
        print(itemSeq)
        search_result = self.search('1', '', '', itemSeq, '')
        print(search_result)
        multi_result = self.multi_info(itemSeq)
        print(multi_result)
        if self.is_json_key_present(multi_result["body"], "items"): # 병용 금기 정보가 있을 경우
            detail_result = search_result["items"][0] + multi_result["body"]["items"]
        else:   # 병용 금기 정보가 없을 경우
            detail_result = search_result["items"][0]
        return detail_result
    

    def search(self, pageNo, entpName, itemName, itemSeq, efcyQesitm):  # 약 정보 통신 함수
        params ={'serviceKey' : config.key,
                'pageNo' : pageNo, 
                'numOfRows' : '10', 
                'entpName' : entpName, 
                'itemName' : itemName, 
                'itemSeq' : itemSeq, 
                'efcyQesitm' : efcyQesitm, 
                'useMethodQesitm' : '', 
                'atpnWarnQesitm' : '', 
                'atpnQesitm' : '', 
                'intrcQesitm' : '', 
                'seQesitm' : '', 
                'depositMethodQesitm' : '', 
                'openDe' : '', 
                'updateDe' : '', 
                'type' : 'json' }
        response = requests.get(config.url, params=params)
        return response.json()["body"]


    def dur_info(self, itemSeq):    # dur 정보 통신 함수
        params ={'serviceKey' : config.key,
                'pageNo' : '1', 
                'numOfRows' : '1',
                'type' : 'json',  
                'itemName' : '', 
                'entpName' : '', 
                'start_change_date' : '', 
                'end_change_date' : '', 
                'itemSeq' : itemSeq}
        response = requests.get(config.dur_info_url, params=params)
        response.json()["body"]["items"][0]["ingrCode"]
        return response.json()

    def multi_info(self, itemSeq): # 병용 금기 정보 통신 함수
        params ={'serviceKey' : config.key,
                'pageNo' : '1', 
                'numOfRows' : '100',
                'type' : 'json', 
                'typeName' : '병용금기', 
                'ingrCode' : '', 
                'itemName' : '', 
                'start_change_date' : '', 
                'end_change_date' : '', 
                'itemSeq' : itemSeq}
        response = requests.get(config.multi_url, params=params)
        return response.json()
    
    def is_json_key_present(self, json, key):
        try:
            buf = json[key]
        except KeyError:
            return False

        return True
    