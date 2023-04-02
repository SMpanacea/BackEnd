from abc import ABCMeta, abstractmethod

#userService에서 다루고 있는 함수를 나열하기 위한 추상 클래스
class User_Service(metaclass=ABCMeta):
    @abstractmethod
    def login(self, id, password):  #로그인 함수
        pass

    @abstractmethod
    def logout(self):  #로그아웃 함수
        pass

    @abstractmethod
    def register(self, uid, upw, email, nickname, gender, birth):  #회원가입 함수
        pass

    