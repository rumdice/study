# -*- coding: utf-8 -*-
from src.rdb.repo.repository import RepositoryBase


class GuildMember(RepositoryBase):
    def add_guild_member(self, guild_uid, auid, grade):
        session = self.guild_factory.session(guild_uid)
        with session:
            return session.add_guild_member(guild_uid, auid, grade)

    def get_guild_member(self, guild_uid, member_uid):
        session = self.guild_factory.session(guild_uid)
        with session:
            return session.query_for_one("GuildMemberDAO.get_guild_member", member_uid, guild_uid)

    def del_guild_member(self, guild_uid, member_uid):
        session = self.guild_factory.session(guild_uid)
        with session:
            return session.delete("GuildMemberDAO.del_guild_member", member_uid)

    def update_guild_member_grade(self, guild_uid, member_uid, grade):
        session = self.guild_factory.session(guild_uid)
        with session:
            return session.update("GuildMemberDAO.update_guild_member_grade", guild_uid, member_uid, grade)

    def del_guild_member_all(self, guild_uid):
        session = self.guild_factory.session(guild_uid)
        with session:
            return session.delete("GuildMemberDAO.del_guild_member_all", guild_uid)

    def guild_member_count(self, guild_uid):
        session = self.guild_factory.session(guild_uid)
        with session:
            return session.query_for_value("GuildMemberDAO.guild_member_count", guild_uid)

    def second_master_list(self, guild_uid):
        session = self.guild_factory.session(guild_uid)
        with session:
            return session.query_for_all("GuildMemberDAO.second_master_list", guild_uid)

    def guild_master_delete(self, guild_uid):
        session = self.guild_factory.session(guild_uid)
        with session:
            return session.delete("GuildMemberDAO.guild_master_delete", guild_uid)

    def guild_member_all(self, guild_uid):
        session = self.guild_factory.session(guild_uid)
        with session:
            return session.query_for_all("GuildMemberDAO.guild_member_all", guild_uid)

    def guild_raid_start(self, guild_uid, auid, time):
        session = self.guild_factory.session(guild_uid)
        with session:
            return session.update("GuildMemberDAO.guild_raid_start", auid, time)

    def guild_raid_reward_grade(self, guild_uid, auid, grade, damage):
        session = self.guild_factory.session(guild_uid)
        with session:
            return session.update("GuildMemberDAO.guild_raid_reward_grade", auid, grade, damage)

    def update_guild_raid_record(self, guild_uid, auid, record):
        session = self.guild_factory.session(guild_uid)
        with session:
            return session.update("GuildMemberDAO.update_guild_raid_record", auid, record)

    def guild_raid_record_clear(self, guild_uid, auid):
        session = self.guild_factory.session(guild_uid)
        with session:
            return session.update("GuildMemberDAO.guild_raid_record_clear", auid)

    def guild_raid_reward(self, guild_uid, auid):
        session = self.guild_factory.session(guild_uid)
        with session:
            return session.update("GuildMemberDAO.guild_raid_reward", auid)

    def update_grade_promote_time(self, guild_uid, auid, promote_time):
        session = self.guild_factory.session(guild_uid)
        with session:
            return session.update("GuildMemberDAO.update_grade_promote_time", auid, promote_time)

    def guild_contest_start(self, guild_uid, auid, time):
        session = self.guild_factory.session(guild_uid)
        with session:
            return session.update("GuildMemberDAO.guild_contest_start", auid, time)

    def update_guild_contest_damage_record(self, guild_uid, auid, record):
        session = self.guild_factory.session(guild_uid)
        with session:
            return session.update("GuildMemberDAO.update_guild_contest_damage_record", auid, record)

    # TODO: 길드 포인트가 redis에도 이중 선언 되어있는게 문제임
    def update_guild_point(self, guild_uid, point):
        session = self.guild_factory.session(guild_uid)
        with session:
            return session.update("GuildMemberDAO.update_guild_point", guild_uid, point)

    def update_contest_reward_time(self, guild_uid, auid, time):
        session = self.guild_factory.session(guild_uid)
        with session:
            return session.update("GuildMemberDAO.update_contest_reward_time", guild_uid, auid, time)

