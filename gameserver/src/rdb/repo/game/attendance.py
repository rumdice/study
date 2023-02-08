# -*- coding: utf-8 -*-
from src.rdb.repo.repository import RepositoryBase


class Attendance(RepositoryBase):
    def insert_attendance_info(self, auid, date):
        session = self.game_factory.session(auid)
        with session:
            session.insert("AttendanceDAO.insert_attendance_info", auid, date)
            return

    def get_attendance_info(self, auid):
        session = self.game_factory.session(auid)
        with session:
            return session.query_for_one("AttendanceDAO.get_attendance_info", auid)

    def reward_attendance(self, auid, attend_cnt, reward_date):
        session = self.game_factory.session(auid)
        with session:
            return session.update("AttendanceDAO.reward_attendance", auid, attend_cnt, reward_date)

    def reward_attendance_end(self, auid, end_date):
        session = self.game_factory.session(auid)
        with session:
            return session.update("AttendanceDAO.reward_attendance_end", auid, end_date)

    def event_reward_attendance(self, auid, attend_cnt, reward_date):
        session = self.game_factory.session(auid)
        with session:
            return session.update("AttendanceDAO.event_reward_attendance", auid, attend_cnt, reward_date)

    def event_attendance_end(self, auid, reward_date, end_date):
        session = self.game_factory.session(auid)
        with session:
            return session.update("AttendanceDAO.event_attendance_end", auid, reward_date, end_date)
