# -*- coding: utf-8 -*-
from sqlalchemy import and_, delete, insert, select, update

from src.rdb.sqlsession import Mapper


class ArenaTournamentDAO(Mapper):
    def __init__(self, metadata):
        Mapper.__init__(self, metadata)
        table_name = self.metadata.schema + '.tb_arena_tournament'
        self.tarenatournament = self.tables[table_name]

    def insert_arena_tournament(self, auid, group, target_auid, index, count, point, turn, round):
        query = insert(self.tarenatournament).values(
            auid = auid,
            group = group,
            target_auid = target_auid,
            match_index = index,
            battle_count = count,
            point = point,
            battle_turn = turn,
            round = round
        )
        return query

    def update_arena_tournament(self, auid, group, target_auid, index, round):
        query = update(self.tarenatournament).values(
            group = group,
            target_auid = target_auid,
            match_index = index,
            battle_count = 3,
            point = 0,
            battle_turn = 0,
            round = round,
            reward_rank = 0,
            end_flag = False,
            target_point = 0
        ).where(
            self.tarenatournament.c.auid == auid
        )
        return query

    def get_arena_tournament(self, auid):
        query = select([self.tarenatournament]).where(
            self.tarenatournament.c.auid == auid
        )
        return query

    def update_arena_tournament_battle_start(self, auid, time):
        query = update(self.tarenatournament).values(
            battle_count = self.tarenatournament.c.battle_count - 1,
            battleStartTime = time,
            battleProcessFlag = True
        ).where(
            self.tarenatournament.c.auid == auid
        )
        return query

    def update_arena_tournament_battle_end(self, auid, point, turn):
        query = update(self.tarenatournament).values(
            point = point,
            battle_turn = turn,
            battleProcessFlag = False
        ).where(
            self.tarenatournament.c.auid == auid
        )
        return query

    def update_arena_tournament_battle_target_end(self, auid, point):
        query = update(self.tarenatournament).values(
            target_point = point
        ).where(
            self.tarenatournament.c.auid == auid
        )
        return query

    def update_arena_tournament_rank(self, auid, rank):
        query = update(self.tarenatournament).values(
            reward_rank = rank,
            end_flag = False
        ).where(
            self.tarenatournament.c.auid == auid
        )
        return query
