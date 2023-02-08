# -*- coding: utf-8 -*-
from src.rdb.repo.repository import RepositoryBase


class TradeItem(RepositoryBase):
    def insert_tradeitems(self, auid, building_uid, refreshTime):
        session = self.game_factory.session(auid)
        with session:
            return session.insert("TradeItemDAO.insert_tradeitems", auid, building_uid, refreshTime)

    def get_tradeitems(self, auid, building_uid):
        session = self.game_factory.session(auid)
        with session:
            return session.query_for_one("TradeItemDAO.get_tradeitems", auid, building_uid)

    def update_tradeitems(self, auid, building_uid, item1, item2, item3, item4, refreshTime):
        session = self.game_factory.session(auid)
        with session:
            return session.update("TradeItemDAO.update_tradeitems", auid, building_uid, item1, item2, item3, item4, refreshTime)

    def update_tradeitem_column(self, auid, building_uid, update_column, column_data):
        session = self.game_factory.session(auid)
        with session:
            update_column += ("='%s'") % column_data
            key = ("auid=%s and building_uid=%s") % (auid, building_uid)
            return session.update_column_doublekey("tb_tradeitem", key,  update_column)