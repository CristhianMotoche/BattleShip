from abc import ABCMeta, abstractmethod


class ModelOperator(metaclass=ABCMeta):
    @abstractmethod
    def lookup(id):
        pass
