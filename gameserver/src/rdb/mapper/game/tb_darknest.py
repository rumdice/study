# -*- coding: utf-8 -*-
from sqlalchemy import and_, delete, func, insert, select, update

from src.rdb.sqlsession import Mapper


class DarknestDAO(Mapper):
    def __init__(self, metadata):
        Mapper.__init__(self, metadata)
        table_name = self.metadata.schema + '.tb_darknest'
        self.tdarknest = self.tables[table_name]

    def insert_darknest_info(self, auid, boss_id, time, boss_infos):
        query = insert(self.tdarknest).values(
            auid = auid,
            boss_id = boss_id,
            respawn_time = time,
            boss_infos = boss_infos
        )
        return query

    def get_darknest_info(self, auid):
        query = select([self.tdarknest]).where(
            self.tdarknest.c.auid == auid
        )
        return query

    def update_darknest_info(self, auid, boss_id, time, boss_infos):
        query = update(self.tdarknest).values(
            boss_id = boss_id,
            respawn_time = time,
            boss_infos = boss_infos
        ).where(
            self.tdarknest.c.auid == auid
        )
        return query

    def update_darknest_clear(self, auid, clear_flag):
        query = update(self.tdarknest).values(
            last_clear = clear_flag
        ).where(
            self.tdarknest.c.auid == auid
        )
        return query

    def update_darknest_level(self, auid, boss_infos):
        query = update(self.tdarknest).values(
            boss_infos = boss_infos,
            last_clear = False
        ).where(
            self.tdarknest.c.auid == auid
        )
        return query

