# -*- coding: utf-8 -*-
from sqlalchemy import and_, delete, insert, select, update

from src.rdb.sqlsession import Mapper


class EventDungeonDAO(Mapper):
    def __init__(self, metadata):
        Mapper.__init__(self, metadata)
        table_name = self.metadata.schema + '.event_dungeon'
        self.teventdungeon = self.tables[table_name]

    def get_event_dungeon(self, uid):
        query = select([self.teventdungeon]).where(self.teventdungeon.c.uid == uid)
        return query

    def get_event_dungeon_all(self):
        query = select([self.teventdungeon])
        return query

    def delete_event_dungeon(self, uids):
        query = delete(self.teventdungeon).where(self.teventdungeon.c.uid.in_(uids))
        return query

