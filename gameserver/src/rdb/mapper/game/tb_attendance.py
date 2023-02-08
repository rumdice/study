# -*- coding: utf-8 -*-
from sqlalchemy import and_, delete, insert, select, update

from src.rdb.sqlsession import Mapper


class AttendanceDAO(Mapper):
    def __init__(self, metadata):
        Mapper.__init__(self, metadata)
        table_name = self.metadata.schema + '.tb_attendance'
        self.tattendance = self.tables[table_name]

    def insert_attendance_info(self, auid, date):
        query = insert(self.tattendance).values(
            auid = auid,
            attend_reward_date = date
        )
        return query

    def get_attendance_info(self, auid):
        query = select([self.tattendance]).where(
            self.tattendance.c.auid == auid
        )
        return query

    def reward_attendance(self, auid, cnt, date):
        query = update(self.tattendance).values(
            attend_cnt = cnt,
            attend_reward_date = date
        ).where(
            self.tattendance.c.auid == auid
        )
        return query

    def reward_attendance_end(self, auid, date):
        query = update(self.tattendance).values(
            attend_end_date = date
        ).where(
            self.tattendance.c.auid == auid
        )
        return query

    def event_reward_attendance(self, auid, cnt, date):
        query = update(self.tattendance).values(
            event_attend = cnt,
            event_reward_date = date
        ).where(
            self.tattendance.c.auid == auid
        )
        return query

    def event_attendance_end(self, auid, reward_date, end_date):
        query = update(self.tattendance).values(
            event_attend = 0,
            event_reward_date = reward_date,
            event_end_date = end_date
        ).where(
            self.tattendance.c.auid == auid
        )
        return query

