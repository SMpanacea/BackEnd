from abc import ABCMeta, abstractmethod

class Token_Service(metaclass= ABCMeta):
    @abstractmethod
    def generate_token(self, user_id):  #토큰 생성 함수
        pass

    @abstractmethod
    def validate_token(self, token):    #토큰 검증 함수
        pass

    def get_id(self, token):    #토큰에서 아이디 추출 함수
        pass