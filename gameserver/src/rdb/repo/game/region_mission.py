# -*- coding: utf-8 -*-
from src.rdb.repo.repository import RepositoryBase


class RegionMission(RepositoryBase):
    def add_region_mission(self, userid, region, difficulty, reward_list):
        session = self.game_factory.session(userid)
        with session:
            session.insert("RegionMissionDAO.add_region_mission", userid, region, difficulty, reward_list)

    def update_region_mission(self, userid, region, difficulty, reward_list):
        session = self.game_factory.session(userid)
        with session:
            return session.update("RegionMissionDAO.update_region_mission", userid, region, difficulty, reward_list)

    def get_region_mission(self, userid, region, difficulty):
        session = self.game_factory.session(userid)
        with session:
            return session.query_for_one("RegionMissionDAO.get_region_mission", userid, region, difficulty)

    def region_mission_all(self, userid):
        session = self.game_factory.session(userid)
        with session:
            return session.query_for_all("RegionMissionDAO.region_mission_all", userid)