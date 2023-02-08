# -*- coding: utf-8 -*-
from sqlalchemy import and_, delete, insert, select, update

from src.rdb.sqlsession import Mapper


class TerritoryBuildDAO(Mapper):
    def __init__(self, metadata):
        Mapper.__init__(self, metadata)
        table_name = self.metadata.schema + '.tb_territory_build'
        self.tterritorybuild = self.tables[table_name]

    def insert_territory_build(self, auid, uid, type, level, time):
        query = insert(self.tterritorybuild).values(
            uid = uid,
            auid = auid,
            building_type = type,
            build_level = level,
            create_time = time
        )
        return query

    def territory_build_list(self, auid):
        query = select([self.tterritorybuild]).where(
            self.tterritorybuild.c.auid == auid
        )
        return query

    def territory_build_process(self, uid):
        query = select([self.tterritorybuild]).where(
            self.tterritorybuild.c.uid == uid
        )
        return query

    def territory_build_type(self, auid, type):
        query = select([self.tterritorybuild]).where(
            and_(
            self.tterritorybuild.c.auid == auid,
            self.tterritorybuild.c.building_type == type
            )
        )
        return query

    def complete_territory_build(self, uid):
        query = delete(self.tterritorybuild).where(
            self.tterritorybuild.c.uid == uid
        )
        return query

    def territory_build_create_time(self, uid, time):
        query = update(self.tterritorybuild).values(
            create_time = time
        ).where(
            self.tterritorybuild.c.uid == uid
        )
        return query

    def find_territory_build(self, uid):
        query = select([self.tterritorybuild]).where(
            self.tterritorybuild.c.uid == uid
        )
        return query