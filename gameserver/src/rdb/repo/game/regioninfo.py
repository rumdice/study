# -*- coding: utf-8 -*-
from src.rdb.repo.repository import RepositoryBase


class RegionInfo(RepositoryBase):
    def insert_region_info(self, userid):
        session = self.game_factory.session(userid)
        with session:
            session.insert("RegionInfoDAO.insert_region_info", userid)

    def update_region_info(self, userid, region_num, difficulty, step):
        session = self.game_factory.session(userid)
        with session:
            return session.update("RegionInfoDAO.update_region_info", userid, region_num, difficulty, step)

    def select_region_info(self, userid):
        session = self.game_factory.session(userid)
        with session:
            return session.query_for_one("RegionInfoDAO.select_region_info", userid)