# -*- coding: utf-8 -*-
from src.rdb.repo.repository import RepositoryBase


class Territory(RepositoryBase):
    def insert_territory(self, auid, building_type, level, start_time, build_slot):
        session = self.game_factory.session(auid)
        with session:
            result = session.insert(
                "TerritoryDAO.insert_territory",
                auid,
                building_type,
                level,
                start_time,
                build_slot
            )
            if result is None:
                return None

            return result.lastrowid

    def update_territory(self, auid, uid, level, startTime):
        session = self.game_factory.session(auid)
        with session:
            return session.update("TerritoryDAO.update_territory", uid, level, startTime)

    def territory_level_wait(self, auid, uid, level):
        session = self.game_factory.session(auid)
        with session:
            return session.update("TerritoryDAO.territory_level_wait", uid, level)

    def update_reward_time(self, auid, uid, startTime):
        session = self.game_factory.session(auid)
        with session:
            return session.update("TerritoryDAO.update_reward_time", uid, startTime)

    def building_count(self, auid, building_type):
        session = self.game_factory.session(auid)
        with session:
            return session.query_for_value("TerritoryDAO.building_count", auid, building_type)

    def find_building(self, auid, uid):
        session = self.game_factory.session(auid)
        with session:
            return session.query_for_one("TerritoryDAO.find_building", uid)

    def select_all_building(self, auid):
        session = self.game_factory.session(auid)
        with session:
            return session.query_for_all("TerritoryDAO.select_all_building", auid)