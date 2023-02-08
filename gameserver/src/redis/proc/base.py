# -*- coding: utf-8 -*-
class ProcBase(object):
    def __init__(self, factory):
        self.factory = factory

    def redis(self):
        return self.factory.redis()