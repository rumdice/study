# -*- coding: utf-8 -*-
from src.rdb.repo.repository import RepositoryBase


class ArenaTournamentInfo(RepositoryBase):
    def update_arena_total_count(self, total_count):
        session = self.admintool_factory.session()
        with session:
            return session.update("ArenaTournamentInfoDAO.update_arena_total_count", total_count)

    def update_arena_user_count(self, user_count):
        session = self.admintool_factory.session()
        with session:
            return session.update("ArenaTournamentInfoDAO.update_arena_user_count", user_count)

    def update_arena_tournament_day(self, day):
        session = self.admintool_factory.session()
        with session:
            return session.update("ArenaTournamentInfoDAO.update_arena_tournament_day", day)

    def get_arena_tournament_info(self):
        session = self.admintool_factory.session()
        with session:
            return session.query_for_one("ArenaTournamentInfoDAO.get_arena_tournament_info")

    def insert_arena_tournament_info(self, time):
        session = self.admintool_factory.session()
        with session:
            session.insert("ArenaTournamentInfoDAO.insert_arena_tournament_info", time)
            return
