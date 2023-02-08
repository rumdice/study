# -*- coding: utf-8 -*-
from src.rdb.repo.repository import RepositoryBase


class GuildInfo(RepositoryBase):
    def add_guild_info(self, guild_uid, join_level, join_type, guild_msg, element, boss_id, boss_hp):
        session = self.guild_factory.session(guild_uid)
        with session:
            return session.insert(
                "GuildInfoDAO.add_guild_info",
                guild_uid,
                join_level,
                join_type,
                guild_msg,
                element,
                boss_id,
                boss_hp
            )

    def del_guild_info(self, guild_uid):
        session = self.guild_factory.session(guild_uid)
        with session:
            return session.insert("GuildInfoDAO.del_guild_info", guild_uid)

    def find_guild(self, guild_uid):
        session = self.guild_factory.session(guild_uid)
        with session:
            return session.query_for_one("GuildInfoDAO.find_guild", guild_uid)

    def update_member_count(self, guild_uid, member_cnt):
        session = self.guild_factory.session(guild_uid)
        with session:
            return session.update("GuildInfoDAO.update_member_count", guild_uid, member_cnt)

    def update_message(self, guild_uid, msg):
        session = self.guild_factory.session(guild_uid)
        with session:
            return session.update("GuildInfoDAO.update_message", guild_uid, msg)

    def update_guild_info(self, guild_uid, msg=0, join_type=0, join_level=0):
        session = self.guild_factory.session(guild_uid)
        with session:
            return session.update("GuildInfoDAO.update_guild_info", guild_uid, msg, join_type, join_level)

    def regen_contest_monster(self, guild_uid, enemy_guild_uid, boss_id, boss_hp, boss_level):
        session = self.guild_factory.session(guild_uid)
        with session:
            return session.update("GuildInfoDAO.regen_contest_monster", guild_uid, enemy_guild_uid, boss_id, boss_hp, boss_level)

    def update_raid_monster_hp(self, guild_uid, cur_hp):
        session = self.guild_factory.session(guild_uid)
        with session:
            ret = session.update("GuildInfoDAO.update_raid_monster_hp", guild_uid, cur_hp)
            if ret is None:
                return False
            if 0 == ret.rowcount:
                return False
            return True

    def update_contest_monster_hp(self, guild_uid, cur_hp):
        session = self.guild_factory.session(guild_uid)
        with session:
            ret = session.update("GuildInfoDAO.update_contest_monster_hp", guild_uid, cur_hp)
            if ret is None:
                return False
            if 0 == ret.rowcount:
                return False
            return True

    def regen_raid_monster(self, guild_uid, element, monster_id, monster_hp, monster_level, win_count):
        session = self.guild_factory.session(guild_uid)
        with session:
            return session.update(
                "GuildInfoDAO.regen_raid_monster",
                guild_uid,
                element,
                monster_id,
                monster_hp,
                monster_level,
                win_count
            )

    def join_condition_change(self, guild_uid, join_type, join_level):
        session = self.guild_factory.session(guild_uid)
        with session:
            return session.update("GuildInfoDAO.join_condition_change", guild_uid, join_type, join_level)

    def select_random(self, guild_uid):
        session = self.guild_factory.session()
        with session:
            return session.query_one_or_none("GuildInfoDAO.select_random", guild_uid)

    def get_guild_all(self):
        session = self.guild_factory.session()
        with session:
            return session.query_for_all("GuildInfoDAO.get_guild_all")

    def update_contest_enemy_guild(self, guild_uid, enemy_guild_uid, contest_monster, contest_element, contest_monster_hp, contest_monster_level, contest_complete_count):
        session = self.guild_factory.session()
        with session:
            return session.update(
                "GuildInfoDAO.update_contest_enemy_guild",
                guild_uid,
                enemy_guild_uid,
                contest_monster,
                contest_element,
                contest_monster_hp,
                contest_monster_level,
                contest_complete_count
            )
