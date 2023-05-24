from abc import ABCMeta, abstractmethod

#userService에서 다루고 있는 함수를 나열하기 위한 추상 클래스
class User_Service(metaclass=ABCMeta):
    @abstractmethod
    def login(self, id, pw):  #로그인 함수
        pass

    @abstractmethod
    def easylogin(self, user):  #간편로그인 함수
        pass

    @abstractmethod
    def token_login(self, token):   #토큰 로그인 함수
        pass

    @abstractmethod
    def update(self, user):  #회원정보 추가 및 수정 함수
        pass

    @abstractmethod
    def withdrawal(self, token):  #회원탈퇴 함수
        pass

    @abstractmethod
    def overlap_check(self, key, value):    #중복체크 함수
        pass

    @abstractmethod
    def find_id(self, user):  #아이디 찾기 함수
        pass

    @abstractmethod
    def find_pw(self, user):  #비밀번호 찾기 함수
        pass

    @abstractmethod
    def info(self, uid): #회원정보 조회 함수
        pass
