# -*- coding: utf-8 -*-
from sqlalchemy import and_, delete, func, insert, select, update

from src.rdb.sqlsession import Mapper


class DeckDAO(Mapper):
    def __init__(self, metadata):
        Mapper.__init__(self, metadata)
        table_name = self.metadata.schema + '.tb_deck'
        self.tdeck = self.tables[table_name]

    def insert_deck_info(self, auid, formation):
        query = insert(self.tdeck).values(
            auid = auid,
            formation = formation,
        )
        
        return query

    def update_deck_info(self, auid, formation, idx, hero_uid):
        if idx == 1:
            query = update(self.tdeck).values(
                formation = formation,
                huid1 = hero_uid
            ).where(
                self.tdeck.c.auid == auid
            )
        elif idx == 2:
            query = update(self.tdeck).values(
                formation = formation,
                huid2 = hero_uid
            ).where(
                self.tdeck.c.auid == auid
            )
        elif idx == 3:
            query = update(self.tdeck).values(
                formation = formation,
                huid3 = hero_uid
            ).where(
                self.tdeck.c.auid == auid
            )
        elif idx == 4:
            query = update(self.tdeck).values(
                formation = formation,
                huid4 = hero_uid
            ).where(
                self.tdeck.c.auid == auid
            )
        elif idx == 5:
            query = update(self.tdeck).values(
                formation = formation,
                huid5 = hero_uid
            ).where(
                self.tdeck.c.auid == auid
            )

        return query

    def get_deck_info(self, auid):
        query = select([self.tdeck]).where(
            and_(
            self.tdeck.c.auid == auid,
            )
        )
        return query
