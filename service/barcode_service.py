from abc import ABCMeta, abstractmethod

class Barcode_Service(metaclass=ABCMeta):

    @abstractmethod
    def search(self, barcode):
        pass