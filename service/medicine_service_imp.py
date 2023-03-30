import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from service.medicine_service import Medicine_Service
import secret_key.config as config
import requests

class Medicine_Service_Imp(Medicine_Service):

    def search(self, itemSeq):
        params ={'serviceKey' : config.key,
                'pageNo' : '1', 
                'numOfRows' : '3', 
                'entpName' : '', 
                'itemName' : '', 
                'itemSeq' : itemSeq, 
                'efcyQesitm' : '', 
                'useMethodQesitm' : '', 
                'atpnWarnQesitm' : '', 
                'atpnQesitm' : '', 
                'intrcQesitm' : '', 
                'seQesitm' : '', 
                'depositMethodQesitm' : '', 
                'openDe' : '', 
                'updateDe' : '', 
                'type' : 'xml' }
        response = requests.get(config.url, params=params)
        return response.content
    