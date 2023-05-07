from abc import ABCMeta, abstractmethod

#userService에서 다루고 있는 함수를 나열하기 위한 추상 클래스
class User_Service(metaclass=ABCMeta):
    @abstractmethod
    def login(self, uid, upw):  #로그인 함수
        pass

    @abstractmethod
    def token_login(self, token):   #토큰 로그인 함수
        pass


    @abstractmethod
    def logout(self):  #로그아웃 함수
        pass

    @abstractmethod
    def register(self, uid, upw, email, nickname, gender, birth):  #회원가입 함수
        pass

    @abstractmethod
    def withdrawal(self, uid):  #회원탈퇴 함수
        pass

    @abstractmethod
    def overlap_check(self, key, value):    #중복체크 함수
        pass

    # @abstractmethod
    # def update(self, uid, upw, email, nickname, gender, birth): #회원정보 수정 함수
    #     pass

    # @abstractmethod
    # def info(self, uid): #회원정보 조회 함수
    #     pass
