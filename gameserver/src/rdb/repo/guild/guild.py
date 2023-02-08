# -*- coding: utf-8 -*-
from src.rdb.repo.repository import RepositoryBase


class Guild(RepositoryBase):
    def add_guild(self, guild_name, guild_masteruid, guild_bg, guild_emblem, create_time):
        session = self.guild_factory.session()
        with session:
            rs = session.insert(
                "GuildDAO.add_guild",
                guild_name,
                guild_masteruid,
                guild_bg,
                guild_emblem,
                create_time
            )

            if rs is None:
                return None

            return rs.lastrowid

    def delete_guild(self, guild_uid):
        session = self.guild_factory.session()
        with session:
            return session.delete("GuildDAO.delete_guild", guild_uid)

    def change_master(self, guild_uid, guild_masteruid):
        session = self.guild_factory.session()
        with session:
            return session.update("GuildDAO.change_master", guild_uid, guild_masteruid)

    def get_guild_recommend_list(self, limit_count):
        session = self.guild_factory.session()
        with session:
            return session.query_for_all("GuildDAO.get_guild_recommend_list", limit_count)

    def modify_guild(self, guild_uid, guild_bg, guild_emblem):
        session = self.guild_factory.session()
        with session:
            return session.update("GuildDAO.modify_guild", guild_uid, guild_bg, guild_emblem)

    def get_guild_search_list(self, limit_count, search_key):
        session = self.guild_factory.session()
        with session:
            return session.query_for_all("GuildDAO.get_guild_search_list", limit_count, search_key)

    def select_guild_all(self):
        session = self.guild_factory.session()
        with session:
            return session.query_for_all("GuildDAO.select_guild_all")

    def select_guild(self, guild_uid):
        session = self.guild_factory.session()
        with session:
            return session.query_for_one("GuildDAO.select_guild", guild_uid)
