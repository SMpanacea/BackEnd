import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from service.email_service import EmailService

# 키 값들을 가져오기 위해 사용
import secret_key.config as config
#이메일 인증을 위한 모듈
from flask_mail import Mail, Message
# 이메일 템플릿을 위한 모듈
from flask import render_template

class Email_ServiceImp(EmailService):
    def send_email(self, email):    #이메일 인증번호 전송 함수
        from app import mail    #app.py에서 생성한 mail 객체를 가져옴
        import random   #랜덤한 문자열을 생성하기 위해 사용
        import string   

        #랜덤한 문자열 생성
        random_num = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
        # Message() 함수는 이메일의 제목과 송신자, 수신자 등의 정보를 입력받아 이메일을 구성
        msg = Message('Panacea인증번호입니다', sender=config.MAIL_USERNAME, recipients=[email])
        # 이메일의 내용을 html 형식으로 작성 (email.html 파일 에 인증번호 넘겨줌)
        msg.html = render_template('email.html', num = random_num)
        # 메일 전송
        mail.send(msg)
        # 인증번호 반환
        return random_num