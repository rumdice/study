# -*- coding: utf-8 -*-
from src.rdb.repo.repository import RepositoryBase


class Deck(RepositoryBase):
    def insert_deck_info(self, auid, formation):
        session = self.game_factory.session(auid)
        with session:
            session.insert("DeckDAO.insert_deck_info", auid, formation)
            return

    def update_deck_info(self, auid, formation, idx, hero_uid):
        session = self.game_factory.session(auid)
        with session:
            session.update("DeckDAO.update_deck_info", auid, formation, idx, hero_uid)
            return

    def get_deck_info(self, auid):
        session = self.game_factory.session(auid)
        with session:
            return session.query_for_one("DeckDAO.get_deck_info", auid)
