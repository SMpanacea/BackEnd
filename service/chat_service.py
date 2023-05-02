from abc import ABCMeta, abstractmethod

class Chat_Service(metaclass=ABCMeta):
    
    @abstractmethod
    def chat(self, content):  # 채팅 함수
        pass