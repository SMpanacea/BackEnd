from abc import ABCMeta, abstractmethod

#userService에서 다루고 있는 함수를 나열하기 위한 추상 클래스
class Medicine_Service(metaclass=ABCMeta):

    @abstractmethod
    def list(self, pageNo, entpName, itemName, itemSeq, efcyQesitm):    # 약 목록 함수
        pass

    @abstractmethod
    def detail(self, itemSeq):  #상세보기 함수
        pass

    @abstractmethod
    def search(self, pageNo, entpName, itemName, itemSeq, efcyQesitm):  # 약 정보 통신 함수
        pass

    @abstractmethod
    def dur_info(self, itemSeq):    # dur 정보 통신 함수
        pass

    @abstractmethod
    def multi_info(self, itemSeq): # 병용 금기 정보 통신 함수
        pass

    