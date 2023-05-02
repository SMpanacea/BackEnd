import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from service.chat_service import Chat_Service
import secret_key.config as config


import openai

class Chat_ServiceImp(Chat_Service):

    """ messages=[
        {"role": "system", "content": "You are a helpful assistant."}, 시스템에게 역할을 부여
        {"role": "user", "content": "Who won the world series in 2020?"}, 사용자의 메세지
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."}, 대답
        {"role": "user", "content": "Where was it played?"} 사용자의 메세지
    ] """

    def chat(self, content):  # 채팅 함수

        openai.api_key = config.GPT_KEY

        completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"{content}"}
        ]
        )

        return completion.choices[0].message["content"].strip()