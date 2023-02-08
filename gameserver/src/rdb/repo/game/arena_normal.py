# -*- coding: utf-8 -*-
from src.rdb.repo.repository import RepositoryBase


class ArenaNormal(RepositoryBase):
    def insert_arena_info(self, auid, rank, time, reward_time):
        session = self.game_factory.session(auid)
        with session:
            ret = session.insert("ArenaNormalDAO.insert_arena_info", auid, rank, time, reward_time)
            if ret is None:
                return None

            return ret.lastrowid

    def get_arena_all(self):
        session = self.game_factory.session()
        with session :
            return session.query_for_all("ArenaNormalDAO.get_arena_all")

    def get_arena_info(self, auid):
        session = self.game_factory.session(auid)
        with session:
            return session.query_for_one("ArenaNormalDAO.get_arena_info", auid)

    def set_arena_target(self, auid, target_list):
        session = self.game_factory.session(auid)
        with session:
            return session.update("ArenaNormalDAO.set_arena_target", auid, target_list)

    def set_battle_target(self, auid, target_uid, battle_time):
        session = self.game_factory.session(auid)
        with session:
            return session.update("ArenaNormalDAO.set_battle_target", auid, target_uid, battle_time)

    def clear_battle_target(self, auid):
        session = self.game_factory.session(auid)
        with session:
            return session.update("ArenaNormalDAO.clear_battle_target", auid)

    def arena_battle_end(self, auid, battle_record):
        session = self.game_factory.session(auid)
        with session:
            return session.update("ArenaNormalDAO.arena_battle_end", auid, battle_record)

    def arena_battle_end_change_rank(self, auid, rank, battle_record):
        session = self.game_factory.session(auid)
        with session:
            return session.update("ArenaNormalDAO.arena_battle_end_change_rank", auid, rank, battle_record)

    def update_arena_reward_time(self, auid, reward_time):
        session = self.game_factory.session(auid)
        with session:
            return session.update("ArenaNormalDAO.update_arena_reward_time", auid, reward_time)

    def update_arena_rank(self, auid, rank):
        session = self.game_factory.session(auid)
        with session:
            return session.update("ArenaNormalDAO.update_arena_rank", auid, rank)
