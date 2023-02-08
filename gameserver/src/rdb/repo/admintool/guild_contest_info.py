# -*- coding: utf-8 -*-
from src.rdb.repo.repository import RepositoryBase


class GuildContestInfo(RepositoryBase):
    def get_guild_contest_info(self):
        session = self.admintool_factory.session()
        with session:
            return session.query_for_one("GuildContestInfoDAO.get_guild_contest_info")
