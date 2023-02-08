# -*- coding: utf-8 -*-
from sqlalchemy import and_, insert, select, update

from src.rdb.sqlsession import Mapper


class ArenaNormalDAO(Mapper):
    def __init__(self, metadata):
        Mapper.__init__(self, metadata)
        table_name = self.metadata.schema + '.tb_arena_normal'
        self.tarenanormal = self.tables[table_name]

    def insert_arena_info(self, auid, rank, time, reward_time):
        query = insert(self.tarenanormal).values(
            auid = auid,
            rank = rank,
            refresh_time = time,
            target_list = '[]',
            reward_time = reward_time,
            battle_record = '[]'
        )
        return query

    def get_arena_all(self):
        query = select([self.tarenanormal])
        return query

    def get_arena_info(self, auid):
        query = select([self.tarenanormal]).where(
            self.tarenanormal.c.auid == auid
        )
        return query

    def set_arena_target(self, auid, target_list):
        query = update(self.tarenanormal).values(
            target_list = target_list
        ).where(
            self.tarenanormal.c.auid == auid
        )
        return query

    def set_battle_target(self, auid, target_uid, time):
        query = update(self.tarenanormal).values(
            battle_target_uid = target_uid,
            battle_start_time = time,
        ).where(
            and_(
            self.tarenanormal.c.auid == auid, 
            self.tarenanormal.c.battle_target_uid == 0
            )
        )
        return query

    def clear_battle_target(self, auid):
        query = update(self.tarenanormal).values(
            battle_target_uid = 0
        ).where(
            self.tarenanormal.c.auid == auid
        )
        return query

    def arena_battle_end(self, auid, record):
        query = update(self.tarenanormal).values(
            battle_target_uid = 0,
            battle_record = record
        ).where(
            self.tarenanormal.c.auid == auid
        )
        return query

    def arena_battle_end_change_rank(self, auid, rank, record):
        query = update(self.tarenanormal).values(
            rank = rank,
            battle_target_uid = 0,
            battle_record = record
        ).where(
            self.tarenanormal.c.auid == auid
        )
        return query

    def update_arena_reward_time(self, auid, time):
        query = update(self.tarenanormal).values(
            reward_time = time
        ).where(
            self.tarenanormal.c.auid == auid
        )
        return query

    def update_arena_rank(self, auid, rank):
        query = update(self.tarenanormal).values(
            rank = rank
        ).where(
            self.tarenanormal.c.auid == auid
        )
        return query