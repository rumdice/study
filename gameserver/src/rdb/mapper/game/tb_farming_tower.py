# -*- coding: utf-8 -*-
from sqlalchemy import and_, delete, insert, select, update

from src.rdb.sqlsession import Mapper


class FarmingTowerDAO(Mapper):
    def __init__(self, metadata):
        Mapper.__init__(self, metadata)
        table_name = self.metadata.schema + '.tb_farming_tower'
        self.tfarmingtower = self.tables[table_name]

    def find_tower(self, auid, tower_uid):
        query = select([self.tfarmingtower]).where(
            and_(
            self.tfarmingtower.c.auid == auid,
            self.tfarmingtower.c.tower_uid == tower_uid
            )
        )
        return query

    def select_all_tower(self, auid):
        query = select([self.tfarmingtower]).where(
            self.tfarmingtower.c.auid == auid
        )
        return query

    def add_farming_tower(self, auid, tower_uid, tower_id, end_time):
        query = insert(self.tfarmingtower).values(
            auid = auid,
            tower_uid = tower_uid,
            tower_id = tower_id,
            end_time = end_time
        )
        return query

    def update_farming_tower(self, auid, tower_uid, tower_id, end_time):
        query = update(self.tfarmingtower).values(
            tower_id = tower_id,
            end_time = end_time,
            clear_floor = 0
        ).where(
            and_(
            self.tfarmingtower.c.auid == auid,
            self.tfarmingtower.c.tower_uid == tower_uid
            )
        )
        return query

    def update_clear_floor(self, auid, tower_uid, clear_floor):
        query = update(self.tfarmingtower).values(
            clear_floor = clear_floor
        ).where(
            and_(
            self.tfarmingtower.c.auid == auid,
            self.tfarmingtower.c.tower_uid == tower_uid
            )
        )
        return query