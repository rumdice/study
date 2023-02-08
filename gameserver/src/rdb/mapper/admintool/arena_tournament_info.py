# -*- coding: utf-8 -*-
from sqlalchemy import and_, delete, insert, select, update

from src.rdb.sqlsession import Mapper


class ArenaTournamentInfoDAO(Mapper):
    def __init__(self, metadata):
        Mapper.__init__(self, metadata)
        table_name = self.metadata.schema + '.arena_tournament_info'
        self.tarenatournamentinfo = self.tables[table_name]

    def update_arena_total_count(self, total_count):
        query = update(self.tarenatournamentinfo).values(total_count=total_count).where(
            self.tarenatournamentinfo.c.uid == 1)
        return query

    def update_arena_user_count(self, user_count):
        query = update(self.tarenatournamentinfo).values(user_count=user_count).where(
            self.tarenatournamentinfo.c.uid == 1)
        return query

    def update_arena_tournament_day(self, day):
        query = update(self.tarenatournamentinfo).values(round_day=day).where(
            self.tarenatournamentinfo.c.uid == 1)
        return query

    def get_arena_tournament_info(self):
        query = select([self.tarenatournamentinfo]).where(self.tarenatournamentinfo.c.uid == 1)
        return query

    def insert_arena_tournament_info(self, time):
        query = insert(self.tarenatournamentinfo).values(uid=1, group=0, day=0, total_count=0, start_time=time)
        return query