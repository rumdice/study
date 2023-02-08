# -*- coding: utf-8 -*-
from sqlalchemy import and_, delete, insert, select, update

from src.rdb.sqlsession import Mapper


class TradeItemDAO(Mapper):
    def __init__(self, metadata):
        Mapper.__init__(self, metadata)
        table_name = self.metadata.schema + '.tb_tradeitem'
        self.ttradeitem = self.tables[table_name]

    def insert_tradeitems(self, auid, building_uid, refreshTime):
        query = insert(self.ttradeitem).values(
            auid = auid,
            building_uid = building_uid,
            trade_item1 = '[]',
            trade_item2 = '[]',
            trade_item3 = '[]',
            trade_item4 = '[]',
            refresh_time = refreshTime
        )
        return query

    def get_tradeitems(self, auid, building_uid):
        query = select([self.ttradeitem]).where(
            and_(
            self.ttradeitem.c.auid == auid,
            self.ttradeitem.c.building_uid == building_uid
            )
        )
        return query

    def update_tradeitems(self, auid, building_uid, item1, item2, item3, item4, refreshTime):
        query = update(self.ttradeitem).values(
            trade_item1 = item1,
            trade_item2 = item2,
            trade_item3 = item3,
            trade_item4 = item4,
            refresh_time = refreshTime
        ).where(
            and_(
            self.ttradeitem.c.auid == auid,
            self.ttradeitem.c.building_uid == building_uid
            )
        )
        return query