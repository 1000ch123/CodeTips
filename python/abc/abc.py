# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod


class Base(metaclass=ABCMeta):

    @abstractmethod
    def _greeting(self):
        print('base')


class Man(Base):
    def _greeting(self):
        print('hello')

if __name__ == '__main__':
    b = Base()
    b._greeting()
    m = Man()
    m._greeting()
