from abc import ABCMeta, abstractmethod

class Email_Service(metaclass=ABCMeta):
    
    @abstractmethod
    def send_email(self, email):    #이메일 인증번호 전송 함수
        pass