# -*- coding: utf-8 -*-
from sqlalchemy import and_, delete, insert, select, update

from src.rdb.sqlsession import Mapper


class EndlessTowerDAO(Mapper):
    def __init__(self, metadata):
        Mapper.__init__(self, metadata)
        table_name = self.metadata.schema + '.tb_endless_tower'
        self.tendlesstower = self.tables[table_name]

    def select_tower(self, auid):
        query = select([self.tendlesstower]).where(
            self.tendlesstower.c.auid == auid
        )
        return query

    def add_endless_tower(self, auid):
        query = insert(self.tendlesstower).values(
            auid = auid
        )
        return query

    def update_clear_floor(self, auid, clear_floor):
        query = update(self.tendlesstower).values(
            clear_floor = clear_floor
        ).where(
            self.tendlesstower.c.auid == auid
        )
        return query