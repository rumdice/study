# -*- coding: utf-8 -*-
from src.redis.proc.base import ProcBase


class EventProc(ProcBase):
    def __init__(self, factory):
        ProcBase.__init__(self, factory)

    def insert_event(self, key, dungeon_id, type, start_time, end_time):
        self.factory.redis().hset(
            key,
            mapping = {
                'UID': key,
                'ID': dungeon_id,
                'TYPE': type,
                'START_TIME': start_time,
                'END_TIME': end_time
            }
        )

    def get_event_list(self):
        return list(self.factory.redis().keys())

    def get_event_info(self, key):
        return self.factory.redis().hgetall(key)

    def clear(self):
        self.factory.redis().flushdb()
