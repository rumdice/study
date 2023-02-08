# -*- coding: utf-8 -*-
from src.rdb.repo.repository import RepositoryBase


class EventDungeonAdmin(RepositoryBase):
    def get_event_dungeon(self, uid):
        session = self.admintool_factory.session()
        with session:
            return session.query_for_one("EventDungeonDAO.get_event_dungeon", uid)

    def get_event_dungeon_all(self):
        session = self.admintool_factory.session()
        with session:
            return session.query_for_all("EventDungeonDAO.get_event_dungeon_all")

    def delete_event_dungeon(self, uids):
        session = self.admintool_factory.session()
        with session:
            session.delete("EventDungeonDAO.delete_event_dungeon", uids)
            return
