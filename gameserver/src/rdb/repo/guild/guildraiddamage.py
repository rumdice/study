# -*- coding: utf-8 -*-
from src.rdb.repo.repository import RepositoryBase


class GuildRaidDamage(RepositoryBase):
    def add_guild_raid_damage(self, guild_uid, auid, damage):
        session = self.guild_factory.session(guild_uid)
        with session:
            return session.add_guild_raid_damage(guild_uid, auid, damage)

    def add_guild_member_damage(self, member_uid, guild_uid):
        session = self.guild_factory.session(guild_uid)
        with session:
            return session.query_for_one("GuildRaidDamageDAO.get_guild_member_damage", member_uid, guild_uid)

    def get_guild_member_damage(self, member_uid, guild_uid):
        session = self.guild_factory.session(guild_uid)
        with session:
            return session.query_for_one("GuildRaidDamageDAO.get_guild_member_damage", member_uid, guild_uid)

    def get_guild_total_damage(self, guild_uid):
        session = self.guild_factory.session(guild_uid)
        with session:
            return session.query_for_sum("GuildRaidDamageDAO.get_guild_total_damage", guild_uid)

    def get_guild_damage_list(self, guild_uid):
        session = self.guild_factory.session(guild_uid)
        with session:
            return session.query_for_all("GuildRaidDamageDAO.get_guild_damage_list", guild_uid)

    def guild_damage_reset(self, guild_uid):
        session = self.guild_factory.session(guild_uid)
        with session:
            return session.delete("GuildRaidDamageDAO.raid_damage_clear")