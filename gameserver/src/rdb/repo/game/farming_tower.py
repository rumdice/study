# -*- coding: utf-8 -*-
from src.rdb.repo.repository import RepositoryBase


class FarmingTower(RepositoryBase):
    def find_tower(self, auid, tower_uid):
        session = self.game_factory.session(auid)
        with session:
            return session.query_for_one("FarmingTowerDAO.find_tower", auid, tower_uid)

    def select_all_tower(self, auid):
        session = self.game_factory.session(auid)
        with session:
            return session.query_for_all("FarmingTowerDAO.select_all_tower", auid)

    def add_farming_tower(self, auid, tower_uid, tower_id, end_time):
        session = self.game_factory.session(auid)
        with session:
            return session.insert("FarmingTowerDAO.add_farming_tower", auid, tower_uid, tower_id, end_time)

    def update_farming_tower(self, auid, tower_uid, tower_id, end_time):
        session = self.game_factory.session(auid)
        with session:
            return session.update("FarmingTowerDAO.update_farming_tower", auid, tower_uid, tower_id, end_time)

    def update_clear_floor(self, auid, tower_uid, clear_floor):
        session = self.game_factory.session(auid)
        with session:
            return session.update("FarmingTowerDAO.update_clear_floor", auid, tower_uid, clear_floor)
