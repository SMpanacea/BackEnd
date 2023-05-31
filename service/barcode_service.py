from abc import ABCMeta, abstractmethod

class Barcode_Service(metaclass=ABCMeta):

    # 바코드 api 검색
    @abstractmethod
    def search(self, barcode):
        pass
    
    # 크롤링
    @abstractmethod
    def crawling_search(self, barcode):
        pass