from abc import ABCMeta, abstractmethod

#userService에서 다루고 있는 함수를 나열하기 위한 추상 클래스
class Medicine_Service(metaclass=ABCMeta):

    @abstractmethod
    def search(self, medicine):  # 약 정보 통신 함수
        pass

    @abstractmethod
    def detail(self, itemSeq):  #상세보기 함수
        pass

    @abstractmethod
    def multi_info(self, itemSeq): # 병용 금기 정보 통신 함수
        pass

    @abstractmethod
    def bookmark(self, bookmark): #즐겨찾기 함수
        pass
    
    @abstractmethod
    def bookmark_off(self, bookmark):   # 즐겨찾기 해제 함수
        pass

    @abstractmethod
    def bookmark_list(self, bookmark):   # 즐겨찾기 리스트 함수
        pass

    @abstractmethod
    def camera_search(self, list):  #카메라 검색 함수
        pass