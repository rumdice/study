# -*- coding: utf-8 -*-
from sqlalchemy import and_, delete, insert, select, update

from src.rdb.sqlsession import Mapper


class MakeItemDAO(Mapper):
    def __init__(self, metadata):
        Mapper.__init__(self, metadata)
        table_name = self.metadata.schema + '.tb_make_item'
        self.tmakeitem = self.tables[table_name]

    def add_make_item(self, auid, building_uid, slot, makeitem, endTime):
        query = insert(self.tmakeitem).values(
            auid = auid,
            building_uid = building_uid,
            make_itemid0 = makeitem,
            end_time0 = endTime
        )
        return query

    def update_make_item(self, auid, building_uid, slot, makeitem, endTime):
        if 1 == slot:
            query = update(self.tmakeitem).values(
                make_itemid1 = makeitem,
                end_time1 = endTime
            ).where(
                and_(
                self.tmakeitem.c.auid == auid,
                self.tmakeitem.c.building_uid == building_uid
                )
            )
        elif 2 == slot:
            query = update(self.tmakeitem).values(
                make_itemid2 = makeitem,
                end_time2 = endTime
            ).where(
                and_(
                self.tmakeitem.c.auid == auid,
                self.tmakeitem.c.building_uid == building_uid
                )
            )
        elif 3 == slot:
            query = update(self.tmakeitem).values(
                make_itemid3 = makeitem,
                end_time3 = endTime
            ).where(
                and_(
                self.tmakeitem.c.auid == auid,
                self.tmakeitem.c.building_uid == building_uid
                )
            )
        elif 4 == slot:
            query = update(self.tmakeitem).values(
                make_itemid4 = makeitem,
                end_time4 = endTime
            ).where(
                and_(
                self.tmakeitem.c.auid == auid,
                self.tmakeitem.c.building_uid == building_uid
                )
            )
        elif 5 == slot:
            query = update(self.tmakeitem).values(
                make_itemid5 = makeitem,
                end_time5 = endTime
            ).where(
                and_(
                self.tmakeitem.c.auid == auid,
                self.tmakeitem.c.building_uid == building_uid
                )
            )
        elif 6 == slot:
            query = update(self.tmakeitem).values(
                make_itemid6 = makeitem,
                end_time6 = endTime
            ).where(
                and_(
                self.tmakeitem.c.auid == auid,
                self.tmakeitem.c.building_uid == building_uid
                )
            )
        else:
            query = update(self.tmakeitem).values(
                make_itemid0 = makeitem,
                end_time0 = endTime
            ).where(
                and_(
                self.tmakeitem.c.auid == auid,
                self.tmakeitem.c.building_uid == building_uid
                )
            )
        return query

    def find_make_item(self, auid, building_uid):
        query = select([self.tmakeitem]).where(
            and_(
            self.tmakeitem.c.auid == auid,
            self.tmakeitem.c.building_uid == building_uid
            )
        )
        return query

    def make_item_all(self, auid):
        query = select([self.tmakeitem]).where(
            self.tmakeitem.c.auid == auid
        )
        return query
