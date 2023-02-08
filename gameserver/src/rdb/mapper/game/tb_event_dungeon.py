# -*- coding: utf-8 -*-
from sqlalchemy import and_, delete, insert, select, update

from src.rdb.sqlsession import Mapper


class EventDungeonDAO(Mapper):
    def __init__(self, metadata):
        Mapper.__init__(self, metadata)
        table_name = self.metadata.schema + '.tb_event_dungeon'
        self.teventdungeon = self.tables[table_name]

    def get_event_dungeon_all(self, auid):
        query = select([self.teventdungeon]).where(
            self.teventdungeon.c.auid == auid
        )
        return query

    def get_event_dungeon(self, auid, uid):
        query = select([self.teventdungeon]).where(
            and_(
            self.teventdungeon.c.auid == auid,
            self.teventdungeon.c.dungeon_uid == uid
            )
        )
        return query

    def add_event_dungeon(self, auid, uid, group, type, time):
        query = insert(self.teventdungeon).values(
            auid = auid,
            dungeon_uid = uid,
            dungeon_id = group,
            dungeon_type = type,
            end_time = time,
            use_ids = '[]'
        )
        return query

    def update_event_dungeon(self, auid, uid, param1, param2, ids):
        query = update(self.teventdungeon).values(
            param1 = param1,
            param2 = param2,
            use_ids = ids
        ).where(
            and_(
            self.teventdungeon.c.auid == auid,
            self.teventdungeon.c.dungeon_uid == uid
            )
        )
        return query

    def update_event_dungeon_ids(self, auid, uid, ids):
        query = update(self.teventdungeon).values(
            use_ids = ids
        ).where(
            and_(
            self.teventdungeon.c.auid == auid,
            self.teventdungeon.c.dungeon_uid == uid
            )
        )
        return query

    def reward_event_dungeon(self, auid, uid, reward):
        query = update(self.teventdungeon).values(
            reward_value = reward
        ).where(
            and_(
            self.teventdungeon.c.auid == auid,
            self.teventdungeon.c.dungeon_uid == uid
            )
        )
        return query

    def delete_event_dungeon(self, auid, uid):
        query = delete(self.teventdungeon).where(
            and_(
            self.teventdungeon.c.auid == auid,
            self.teventdungeon.c.dungeon_uid == uid
            )
        )
        return query

    def delete_event_dungeon_all(self, auid):
        query = delete(self.teventdungeon).where(
            self.teventdungeon.c.auid == auid
        )
        return query

    def update_event_dungeon_difficulty(self, auid, uid, param3):
        query = update(self.teventdungeon).values(
            param3 = param3
        ).where(
            and_(
            self.teventdungeon.c.auid == auid,
            self.teventdungeon.c.dungeon_uid == uid
            )
        )
        return query