# -*- coding: utf-8 -*-
from src.rdb.repo.repository import RepositoryBase


class Gacha(RepositoryBase):
    def get_gacha_all(self, auid):
        session = self.game_factory.session(auid)
        with session:
            return session.query_for_all("GachaDAO.get_gacha_all", auid)

    def get_gacha(self, auid, gacha_id):
        session = self.game_factory.session(auid)
        with session:
            return session.query_for_one("GachaDAO.get_gacha", auid, gacha_id)

    def add_gacha(self, auid, gacha_id, time):
        session = self.game_factory.session(auid)
        with session:
            return session.insert("GachaDAO.add_gacha", auid, gacha_id, time)

    def update_gacha_time(self, auid, gacha_id, time):
        session = self.game_factory.session(auid)
        with session:
            return session.update("GachaDAO.update_gacha_time", auid, gacha_id, time)