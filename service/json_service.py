from abc import ABCMeta, abstractmethod

class Json_Service(metaclass=ABCMeta):

    @abstractmethod
    def json_key_check(self, json, key):  # json 통신 결과의 key가 존재하는지 확인하는 함수
        pass