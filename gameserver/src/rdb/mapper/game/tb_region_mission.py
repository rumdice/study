# -*- coding: utf-8 -*-
from sqlalchemy import and_, delete, insert, select, update

from src.rdb.sqlsession import Mapper


class RegionMissionDAO(Mapper):
    def __init__(self, metadata):
        Mapper.__init__(self, metadata)
        table_name = self.metadata.schema + '.tb_region_mission'
        self.tregionmission = self.tables[table_name]

    def add_region_mission(self, userid, region, difficulty, reward_list):
        query = insert(self.tregionmission).values(
            auid = userid,
            region_id = region,
            difficulty = difficulty,
            reward_list = reward_list
        )
        return query

    def update_region_mission(self, userid, region, difficulty, reward_list):
        query = update(self.tregionmission).values(
            reward_list = reward_list
        ).where(
            and_(
            self.tregionmission.c.auid == userid,
            self.tregionmission.c.region_id == region,
            self.tregionmission.c.difficulty == difficulty
            )
        )
        return query

    def get_region_mission(self, userid, region, difficulty):
        query = select([self.tregionmission]).where(
            and_(
            self.tregionmission.c.auid == userid,
            self.tregionmission.c.region_id == region,
            self.tregionmission.c.difficulty == difficulty
            )
        )
        return query

    def region_mission_all(self, userid):
        query = select([self.tregionmission]).where(
            self.tregionmission.c.auid == userid
        )
        return query
