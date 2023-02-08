# -*- coding: utf-8 -*-
from sqlalchemy import and_, delete, func, insert, select, update

from src.rdb.sqlsession import Mapper


class TerritoryDAO(Mapper):
    def __init__(self, metadata):
        Mapper.__init__(self, metadata)
        table_name = self.metadata.schema + '.tb_territory'
        self.tterritory = self.tables[table_name]

    def insert_territory(self, auid, type, level, time, slot):
        query = insert(self.tterritory).values(
            auid = auid,
            building_type = type,
            level = level,
            start_time = time,
            build_slot = slot
        )
        return query

    def update_territory(self, uid, level, time):
        query = update(self.tterritory).values(
            level = level,
            start_time = time
        ).where(
            self.tterritory.c.uid == uid
        )
        return query

    def territory_level_wait(self, uid, level):
        query = update(self.tterritory).values(
            level = level
        ).where(
            self.tterritory.c.uid == uid
        )
        return query

    def update_reward_time(self, uid, time):
        query = update(self.tterritory).values(
            start_time = time
        ).where(
            self.tterritory.c.uid == uid
        )
        return query

    def building_count(self, auid, type):
        query = select([func.count(self.tterritory.c.building_type)]).where(
            and_(
            self.tterritory.c.auid == auid,
            self.tterritory.c.building_type == type
            )
        )
        return query

    def find_building(self, uid):
        query = select([self.tterritory]).where(
            self.tterritory.c.uid == uid)
        return query

    def select_all_building(self, auid):
        query = select([self.tterritory]).where(
            self.tterritory.c.auid == auid
        )
        return query

