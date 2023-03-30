from abc import ABCMeta, abstractmethod

#userService에서 다루고 있는 함수를 나열하기 위한 추상 클래스
class Medicine_Service(metaclass=ABCMeta):
    @abstractmethod
    def search(self, itemSeq):  #검색 함수
        pass

    