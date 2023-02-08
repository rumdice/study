# -*- coding: utf-8 -*-
from src.rdb.repo.repository import RepositoryBase


class ArenaTournament(RepositoryBase):
    def insert_arena_tournament(self, auid, group, target_auid, match_index, battle_count, point, battle_turn, round):
        session = self.game_factory.session(auid)
        with session:
            ret = session.insert(
                "ArenaTournamentDAO.insert_arena_tournament",
                auid,
                group,
                target_auid,
                match_index,
                battle_count,
                point,
                battle_turn,
                round
            )

            if ret is None:
                return None

            return ret.lastrowid

    def update_arena_tournament(self, auid, group, target_auid, match_index, round):
        session = self.game_factory.session(auid)
        with session:
            session.update(
                "ArenaTournamentDAO.update_arena_tournament",
                auid,
                group,
                target_auid,
                match_index,
                round
            )

    def get_arena_tournament(self, auid):
        session = self.game_factory.session(auid)
        with session:
            return session.query_for_one("ArenaTournamentDAO.get_arena_tournament", auid)

    def update_arena_tournament_battle_start(self, auid, time):
        session = self.game_factory.session(auid)
        with session:
            session.update("ArenaTournamentDAO.update_arena_tournament_battle_start", auid, time)

    def update_arena_tournament_battle_end(self, auid, point, battle_trun):
        session = self.game_factory.session(auid)
        with session:
            session.update("ArenaTournamentDAO.update_arena_tournament_battle_end", auid, point, battle_trun)

    def update_arena_tournament_battle_target_end(self, auid, point):
        session = self.game_factory.session(auid)
        with session:
            session.update("ArenaTournamentDAO.update_arena_tournament_battle_target_end", auid, point)

    def update_arena_tournament_rank(self, auid, rank):
        session = self.game_factory.session(auid)
        with session:
            session.update("ArenaTournamentDAO.update_arena_tournament_rank", auid, rank)