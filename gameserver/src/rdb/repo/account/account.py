# -*- coding: utf-8 -*-
from src.rdb.repo.repository import RepositoryBase


class Account(RepositoryBase):
    def find_web_userid(self, web_userid):
        session = self.account_factory.session()
        with session:
            return session.query_for_one("AccountDAO.find_web_userid", web_userid)

    def insert_account(self, account_type, user_token, nickname, device_info, create_time, email):
        session = self.account_factory.session()
        with session:
            rs = session.insert(
                "AccountDAO.insert_account",
                account_type,
                user_token,
                nickname,
                device_info,
                create_time,
                email
            )

            if rs is None:
                return None

            return rs.lastrowid

    def update_last_login(self, userid, time):
        session = self.account_factory.session()
        with session:
            session.update(
                "AccountDAO.update_last_login",
                userid,
                time
            )

    def select_all_account(self):
        session = self.account_factory.session()
        with session:
            return session.query_for_all("AccountDAO.select_all_account")

    def delete_account_devlop(self, user_token):
        session = self.account_factory.session()
        with session:
            account_info = session.query_for_one("AccountDAO.find_web_userid", user_token)
            if account_info is None:
                return 0

            session.delete("AccountDAO.delete_account", account_info.account_uid)
            return account_info.account_uid

    def find_user_nickname(self, nick_name):
        session = self.account_factory.session()
        with session:
            return session.query_for_one("AccountDAO.find_user_nickname", nick_name)

    def change_user_nickname(self, userid, change_nickname):
        session = self.account_factory.session()
        with session:
            return session.update("AccountDAO.change_user_nickname", userid, change_nickname)

    def find_user_id(self, userid):
        session = self.account_factory.session()
        with session:
            return session.query_for_one("AccountDAO.find_user_id", userid)

    def update_alram_agree(self, userid, agree):
        session = self.account_factory.session()
        with session:
            return session.update("AccountDAO.update_alram_agree", userid, agree)

class HallofFame(RepositoryBase):
    def insert_hall_of_fame(self, hall_of_fame_data):
        session = self.account_factory.session()
        with session:
            rs = session.insert("ArenaNormalHallOfFameDAO.insert_hall_of_fame", hall_of_fame_data)
            if rs is None:
                return None

            return rs.lastrowid

    def remove_hall_of_fame(self, uid):
        session = self.account_factory.session()
        with session:
            session.delete("ArenaNormalHallOfFameDAO.remove_hall_of_fame", uid)
