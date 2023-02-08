# -*- coding: utf-8 -*-
from sqlalchemy import and_, delete, func, insert, select, update

from src.protocol.webapp_pb import Define
from src.rdb.sqlsession import Mapper


class GuildMemberDAO(Mapper):
    def __init__(self, metadata):
        Mapper.__init__(self, metadata)
        table_name = self.metadata.schema + '.tb_guild_member'
        self.tguildmember = self.tables[table_name]

    def get_guild_member(self, member_uid, guild_uid):
        query = select([self.tguildmember]).where(
            and_(
            self.tguildmember.c.auid == member_uid,
            self.tguildmember.c.guild_uid == guild_uid
            )
        )
        return query

    def del_guild_member(self, member_uid):
        query = delete(self.tguildmember).where(
            self.tguildmember.c.auid == member_uid
        )
        return query

    def update_guild_member_grade(self, guild_uid, member_uid, grade):
        query = update(self.tguildmember).values(
            guild_grade=grade
        ).where(
            and_(
            self.tguildmember.c.guild_uid == guild_uid,
            self.tguildmember.c.auid == member_uid
            )
        )
        return query

    def del_guild_member_all(self, guild_uid):
        query = delete(self.tguildmember).where(
            self.tguildmember.c.guild_uid == guild_uid
        )
        return query

    def guild_member_count(self, guild_uid):
        query = select([func.count(self.tguildmember.c.guild_uid)]).where(
            and_(
            self.tguildmember.c.guild_uid == guild_uid,
            self.tguildmember.c.guild_grade < Define.GUILD_GRADE_WAIT
            )
        )
        return query

    def second_master_list(self, guild_uid):
        query = select([self.tguildmember]).where(
            and_(
            self.tguildmember.c.guild_uid == guild_uid,
            self.tguildmember.c.guild_grade == Define.GUILD_GRADE_SECOND_MASTER
            )
        )
        query = query.order_by(self.tguildmember.c.grade_promote_time.asc())
        return query

    def guild_member_all(self, guild_uid):
        query = select([self.tguildmember]).where(
            and_(
            self.tguildmember.c.guild_uid == guild_uid,
            self.tguildmember.c.guild_grade != Define.GUILD_GRADE_NONE
            )
        )
        return query

    def guild_master_delete(self, guild_uid):
        query = delete(self.tguildmember).where(
            and_(
            self.tguildmember.c.guild_uid == guild_uid,
            self.tguildmember.c.guild_grade == Define.GUILD_GRADE_MASTER
            )
        )
        return query

    def guild_contest_start(self, auid, time):
        query = update(self.tguildmember).values(
            contest_start_time = time
        ).where(
            self.tguildmember.c.auid == auid
        )
        return query

    def update_guild_contest_damage_record(self, auid, record):
        query = update(self.tguildmember).values(
            contest_damage_record = record
        ).where(
            self.tguildmember.c.auid == auid
        )
        return query

    def guild_raid_start(self, auid, time):
        query = update(self.tguildmember).values(
            raid_start_time = time
        ).where(
            self.tguildmember.c.auid == auid
        )
        return query

    def update_guild_raid_record(self, auid, record):
        query = update(self.tguildmember).values(
            raid_record = record
        ).where(
            self.tguildmember.c.auid == auid
        )
        return query

    def guild_raid_reward_grade(self, auid, grade, damage):
        query = update(self.tguildmember).values(
            reward_grade = grade,
            reward_damage = damage
        ).where(
            self.tguildmember.c.auid == auid
        )
        return query

    def guild_raid_record_clear(self, auid):
        query = update(self.tguildmember).values(
            raid_record = '[]',
            reward_flag = False
        ).where(
            self.tguildmember.c.auid == auid
        )
        return query

    def guild_raid_reward(self, auid):
        query = update(self.tguildmember).values(
            reward_flag = True
        ).where(
            self.tguildmember.c.auid == auid
        )
        return query

    def update_grade_promote_time(self, auid, promote_time):
        query = update(self.tguildmember).values(
            grade_promote_time = promote_time
        ).where(
            self.tguildmember.c.auid == auid
        )
        return query

    def update_guild_point(self, guild_uid, point):
        query = update(self.tguildmember).values(
            guild_point = point
        ).where(
            self.tguildmember.c.guild_uid == guild_uid
        )
        return query

    def update_contest_reward_time(self, guild_uid, auid, time):
        query = update(self.tguildmember).values(
            contest_reward_time = time
        ).where(
            and_(
            self.tguildmember.c.guild_uid == guild_uid,
            self.tguildmember.c.auid == auid
            )
        )
        return query

