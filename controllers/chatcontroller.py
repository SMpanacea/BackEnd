from flask import Blueprint, request

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# 다른 파일에 있는 클래스를 import하기 위해 경로 설정

from service.chat_service_imp import Chat_Service_Imp

chat = Blueprint('chat', __name__)  # Blueprint를 이용하면 controller처럼 사용할 수 있다. 

# ChatGPT 채팅
@chat.route('/question', methods=['POST']) #post 방식만 잡아서 처리한다.
def chatgpt():
    chat_service = Chat_Service_Imp()
    jsonData = request.get_json()
    print(jsonData)
    # 채팅 질문을 받아서 답변을 반환
    return chat_service.chat(jsonData)