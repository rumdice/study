# -*- coding: utf-8 -*-
from sqlalchemy import and_, delete, insert, select, update

from src.rdb.sqlsession import Mapper


class GachaDAO(Mapper):
    def __init__(self, metadata):
        Mapper.__init__(self, metadata)
        table_name = self.metadata.schema + '.tb_gacha'
        self.tgacha = self.tables[table_name]

    def get_gacha_all(self, auid):
        query = select([self.tgacha]).where(
            self.tgacha.c.auid == auid
        )
        return query

    def get_gacha(self, auid, gacha_id):
        query = select([self.tgacha]).where(
            and_(
            self.tgacha.c.auid == auid,
            self.tgacha.c.gacha_id == gacha_id
            )
        )
        return query

    def add_gacha(self, auid, gacha_id, time):
        query = insert(self.tgacha).values(
            auid = auid,
            gacha_id = gacha_id,
            summon_time = time
        )
        return query

    def update_gacha_time(self, auid, gacha_id, time):
        query = update(self.tgacha).values(
            summon_time = time
        ).where(
            and_(
            self.tgacha.c.auid == auid,
            self.tgacha.c.gacha_id == gacha_id
            )
        )
        return query
