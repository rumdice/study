# -*- coding: utf-8 -*-
from sqlalchemy import delete, insert, select, update

from src.rdb.sqlsession import Mapper


class RegionInfoDAO(Mapper):
    def __init__(self, metadata):
        Mapper.__init__(self, metadata)
        table_name = self.metadata.schema + '.tb_region_info'
        self.tregioninfo = self.tables[table_name]

    def insert_region_info(self, userid):
        query = insert(self.tregioninfo).values(
            auid = userid
        )
        return query

    def update_region_info(self, userid, region_num, difficulty, step):
        query = update(self.tregioninfo).values(
            region_num = region_num,
            region_difficulty = difficulty,
            region_step = step
        ).where(
            self.tregioninfo.c.auid == userid
        )
        return query

    def select_region_info(self, userid):
        query = select([self.tregioninfo]).where(
            self.tregioninfo.c.auid == userid
        )
        return query
