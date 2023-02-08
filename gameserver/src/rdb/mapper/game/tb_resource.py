# -*- coding: utf-8 -*-
from sqlalchemy import and_, delete, insert, select, update

from src.rdb.sqlsession import Mapper


class ResourceCollectDAO(Mapper):
    def __init__(self, metadata):
        Mapper.__init__(self, metadata)
        table_name = self.metadata.schema + '.tb_resource_collect'
        self.tresourcecollect = self.tables[table_name]

    def insert_data(self, auid, idx, time):
        query = insert(self.tresourcecollect).values(
            auid = auid,
            resource_idx = idx,
            dispatch_list = '[]',
            start_time = time,
            end_time = time
        )
        return query

    def select_all(self, auid):
        query = select([self.tresourcecollect]).where(
            self.tresourcecollect.c.auid == auid
        )
        return query

    def udpate_data(self, auid, idx, resource_id, lv, dist, dispatch_list, start_time, end_time, resource_max, move_time):
        query = update(self.tresourcecollect).values(
            resource_id = resource_id,
            resource_lv = lv,
            distance = dist,
            dispatch_list = dispatch_list,
            start_time = start_time,
            end_time = end_time,
            resource_max = resource_max,
            move_time = move_time
        ).where(
            and_(
            self.tresourcecollect.c.auid == auid,
            self.tresourcecollect.c.resource_idx == idx
            )
        )
        return query

    def select_idx(self, auid, idx):
        query = select([self.tresourcecollect]).where(
            and_(
            self.tresourcecollect.c.auid == auid,
            self.tresourcecollect.c.resource_idx == idx
            )
        )
        return query

    def update_return_data(self, auid, idx, end_time, resource_max):
        query = update(self.tresourcecollect).values(
            end_time = end_time,
            resource_max = resource_max,
            move_time = 0
        ).where(
            and_(
            self.tresourcecollect.c.auid == auid,
            self.tresourcecollect.c.resource_idx == idx
            )
        )
        return query

    def clear_data(self, auid, idx):
        query = update(self.tresourcecollect).values(
            resource_id = 0,
            resource_lv = 0,
            distance = 0,
            dispatch_list = '[]',
            resource_max = 0,
            move_time = 0
        ).where(
            and_(
            self.tresourcecollect.c.auid == auid,
            self.tresourcecollect.c.resource_idx == idx
            )
        )
        return query


class ResourceDispatchDAO(Mapper):
    def __init__(self, metadata):
        Mapper.__init__(self, metadata)
        table_name = self.metadata.schema + '.tb_resource_dispatch'
        self.tresourcedispatch = self.tables[table_name]

    def insert_data(self, auid, idx, id, level, dist):
        query = insert(self.tresourcedispatch).values(
            auid = auid,
            resource_idx = idx,
            resource_id = id,
            resource_lv = level,
            distance = dist
        )
        return query

    def select_all(self, auid):
        query = select([self.tresourcedispatch]).where(
            self.tresourcedispatch.c.auid == auid
        )
        return query

    def udpate_data(self, auid, idx, id, level, dist):
        query = update(self.tresourcedispatch).values(
            resource_id = id,
            resource_lv = level,
            distance = dist
        ).where(
            and_(
            self.tresourcedispatch.c.auid == auid,
            self.tresourcedispatch.c.resource_idx == idx
            )
        )
        return query

    def select_idx(self, auid, idx):
        query = select([self.tresourcedispatch]).where(
            and_(
            self.tresourcedispatch.c.auid == auid,
            self.tresourcedispatch.c.resource_idx == idx
            )
        )
        return query

    def clear_data(self, auid, idx):
        query = update(self.tresourcedispatch).values(
            resource_id = 0,
            resource_lv = 0,
            distance = 0
        ).where(
            and_(
            self.tresourcedispatch.c.auid == auid,
            self.tresourcedispatch.c.resource_idx == idx
            )
        )
        return query