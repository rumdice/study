# -*- coding: utf-8 -*-
from src.rdb.repo.repository import RepositoryBase


class RaidResult(RepositoryBase):
    def add_raid_result(self, guild_uid):
        session = self.guild_factory.session(guild_uid)
        with session:
            return session.insert("RaidResultDAO.add_raid_result", guild_uid)

    def del_raid_result(self, guild_uid):
        session = self.guild_factory.session(guild_uid)
        with session:
            return session.insert("RaidResultDAO.del_raid_result", guild_uid)

    def find_raid_result(self, guild_uid):
        session = self.guild_factory.session(guild_uid)
        with session:
            return session.query_for_one("RaidResultDAO.find_raid_result", guild_uid)

    def update_raid_result(self, guild_uid, monster_id, element, cur_hp, level, damage_record):
        session = self.guild_factory.session(guild_uid)
        with session:
            return session.update("RaidResultDAO.update_raid_result", guild_uid, monster_id, element, cur_hp, level, damage_record)

