# -*- coding: utf-8 -*-
from src.rdb.repo.repository import RepositoryBase


class EndlessTower(RepositoryBase):
    def find_tower(self, auid):
        session = self.game_factory.session(auid)
        with session:
            return session.query_for_one("EndlessTowerDAO.find_tower", auid)

    def add_endless_tower(self, auid):
        session = self.game_factory.session(auid)
        with session:
            return session.insert("EndlessTowerDAO.add_endless_tower", auid)

    def select_tower(self, auid):
        session = self.game_factory.session(auid)
        with session:
            return session.query_for_all("EndlessTowerDAO.select_tower", auid)

    def update_clear_floor(self, auid, clear_floor):
        session = self.game_factory.session(auid)
        with session:
            return session.update("EndlessTowerDAO.update_clear_floor", auid, clear_floor)
