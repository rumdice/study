# -*- coding: utf-8 -*-
from src.rdb.repo.repository import RepositoryBase


class MakeItem(RepositoryBase):
    def add_make_item(self, auid, building_uid, slot, makeitem, endTime):
        session = self.game_factory.session(auid)
        with session:
            return session.insert("MakeItemDAO.add_make_item", auid, building_uid, slot, makeitem, endTime)

    def update_make_item(self, auid, building_uid, slot, makeitem, endTime):
        session = self.game_factory.session(auid)
        with session:
            return session.update("MakeItemDAO.update_make_item", auid, building_uid, slot, makeitem, endTime)

    def find_make_item(self, auid, building_uid):
        session = self.game_factory.session(auid)
        with session:
            return session.query_for_one("MakeItemDAO.find_make_item", auid, building_uid)

    def make_item_all(self, auid):
        session = self.game_factory.session(auid)
        with session:
            return session.query_for_all("MakeItemDAO.make_item_all", auid)