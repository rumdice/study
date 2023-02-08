# -*- coding: utf-8 -*-
from src.rdb.repo.repository import RepositoryBase


class Darknest(RepositoryBase):
    def insert_darknest_info(self, auid, boss_id, respawn_time, boss_ifnos):
        session = self.game_factory.session(auid)
        with session:
            session.insert("DarknestDAO.insert_darknest_info", auid, boss_id, respawn_time, boss_ifnos)
            return

    def get_darknest_info(self, auid):
        session = self.game_factory.session(auid)
        with session:
            return session.query_for_one("DarknestDAO.get_darknest_info", auid)

    def update_darknest_info(self, auid, boss_id, respawn_time, boss_ifnos):
        session = self.game_factory.session(auid)
        with session:
            return session.update("DarknestDAO.update_darknest_info", auid, boss_id, respawn_time, boss_ifnos)

    def update_darknest_clear(self, auid, clear_flag):
        session = self.game_factory.session(auid)
        with session:
            return session.update("DarknestDAO.update_darknest_clear", auid, clear_flag)

    def update_darknest_level(self, auid, boss_infos):
        session = self.game_factory.session(auid)
        with session:
            return session.update("DarknestDAO.update_darknest_level", auid, boss_infos)
