# -*- coding: utf-8 -*-
from src.rdb.repo.repository import RepositoryBase


class Post(RepositoryBase):
    def send_post(self, auid, post_type, title_msg, post_msg, post_item, remove_time, keep_day):
        session = self.game_factory.session(auid)
        with session:
            return session.insert("PostDAO.send_post", auid, post_type, title_msg, post_msg, post_item, remove_time, keep_day)

    def post_count(self, auid):
        session = self.game_factory.session(auid)
        with session:
            return session.query_for_value("PostDAO.post_count", auid)

    def get_post_list(self, auid):
        session = self.game_factory.session(auid)
        with session:
            return session.query_for_all("PostDAO.get_post_list", auid)

    def get_post_with_title(self, auid, title):
        session = self.game_factory.session(auid)
        with session:
            return session.query_for_one("PostDAO.get_post_with_title", auid, title)

    def remove_post(self, auid, uids):
        session = self.game_factory.session(auid)
        with session:
            return session.delete("PostDAO.remove_post", uids)

    def receive_post(self, auid, uid):
        session = self.game_factory.session(auid)
        with session:
            return session.update("PostDAO.receive_post", uid)

    def get_post_uids(self, auid, uids):
        session = self.game_factory.session(auid)
        with session:
            return session.query_for_all("PostDAO.get_post_uids", uids)

    def reward_post_uids(self, auid, uids):
        session = self.game_factory.session(auid)
        with session:
            return session.update("PostDAO.reward_post_uids", uids)
