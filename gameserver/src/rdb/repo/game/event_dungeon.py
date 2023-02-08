# -*- coding: utf-8 -*-
from src.rdb.repo.repository import RepositoryBase


class EventDungeon(RepositoryBase):
    def get_event_dungeon_all(self, auid):
        session = self.game_factory.session(auid)
        with session:
            return session.query_for_all("EventDungeonDAO.get_event_dungeon_all", auid)

    def get_event_dungeon(self, auid, uid):
        session = self.game_factory.session(auid)
        with session:
            return session.query_for_one("EventDungeonDAO.get_event_dungeon", auid, uid)

    def add_event_dungeon(self, auid, uid, group, type, end_time):
        session = self.game_factory.session(auid)
        with session:
            ret = session.insert("EventDungeonDAO.add_event_dungeon", auid, uid, group, type, end_time)
            if ret is None:
                return None

            return ret.lastrowid

    def update_event_dungeon(self, auid, uid, param1, param2, ids):
        session = self.game_factory.session(auid)
        with session:
            return session.update("EventDungeonDAO.update_event_dungeon", auid, uid, param1, param2, ids)

    def update_event_dungeon_ids(self, auid, uid, ids):
        session = self.game_factory.session(auid)
        with session:
            return session.update("EventDungeonDAO.update_event_dungeon_ids", auid, uid, ids)

    def reward_event_dungeon(self, auid, uid, reward):
        session = self.game_factory.session(auid)
        with session:
            return session.update("EventDungeonDAO.reward_event_dungeon", auid, uid, reward)

    def delete_event_dungeon(self, auid, uid):
        session = self.game_factory.session(auid)
        with session:
            return session.delete("EventDungeonDAO.delete_event_dungeon", auid, uid)

    def delete_event_dungeon_all(self, auid):
        session = self.game_factory.session(auid)
        with session:
            return session.delete("EventDungeonDAO.delete_event_dungeon_all", auid)

    def update_event_dungeon_difficulty(self, auid, uid, param3):
        session = self.game_factory.session(auid)
        with session:
            return session.delete("EventDungeonDAO.update_event_dungeon_difficulty", auid, uid, param3)