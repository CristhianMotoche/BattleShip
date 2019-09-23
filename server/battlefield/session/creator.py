import random

from battlefield.session.models import Session
from battlefield.utils.models import ModelOperator


class SessionCreator:

    __CHARS = 'ABCDEFGHIabcdefghi'
    __SIZE_ID = 6

    def __init__(self):
        pass

    def perform(self):
        return Session(self.__get_rand_id())

    def __get_rand_id(self):
        random_keys = []
        for _ in range(self.__SIZE_ID):
            idx = random.randrange(0, len(self.__CHARS))
            random_keys.append(self.__CHARS[idx])
        return ''.join(random_keys)
