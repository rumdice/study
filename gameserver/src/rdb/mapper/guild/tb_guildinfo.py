# -*- coding: utf-8 -*-
from sqlalchemy import and_, delete, insert, select, update
from sqlalchemy.sql.expression import func, select

from src.rdb.sqlsession import Mapper


class GuildInfoDAO(Mapper):
    def __init__(self, metadata):
        Mapper.__init__(self, metadata)
        table_name = self.metadata.schema + '.tb_guildinfo'
        self.tguildinfo = self.tables[table_name]

    def add_guild_info(self, guild_uid, level, type, msg, element, boss_id, boss_hp):
        query = insert(self.tguildinfo).values(
            guild_uid = guild_uid,
            join_level = level,
            join_type = type,
            guild_msg = msg,
            raid_element = element,
            raid_monster = boss_id,
            raid_monster_hp = boss_hp
        )
        return query

    def del_guild_info(self, guild_uid):
        query = delete(self.tguildinfo).where(
            self.tguildinfo.c.guild_uid == guild_uid
        )
        return query

    def get_guild_all(self):
        query = select([self.tguildinfo])
        return query

    def find_guild(self, guild_uid):
        query = select([self.tguildinfo]).where(
            self.tguildinfo.c.guild_uid == guild_uid
        )
        return query

    def update_member_count(self, guild_uid, member_cnt):
        query = update(self.tguildinfo).values(
            member_count=member_cnt
        ).where(
            self.tguildinfo.c.guild_uid == guild_uid
        )
        return query

    def update_message(self, guild_uid, msg):
        query = update(self.tguildinfo).values(
            guild_msg=msg
        ).where(
            self.tguildinfo.c.guild_uid == guild_uid
        )
        return query

    def update_guild_info(self, guild_uid, msg = 0, join_type = 0, join_level = 0):
        query = update(self.tguildinfo).values(
            guild_msg = msg,
            join_type = join_type,
            join_level = join_level
        ).where(
            self.tguildinfo.c.guild_uid == guild_uid
        )
        return query

    def update_raid_monster_hp(self, guild_uid, cur_hp):
        query = update(self.tguildinfo).values(
            raid_monster_hp = cur_hp
        ).where(
            and_(
            self.tguildinfo.c.guild_uid == guild_uid,
            self.tguildinfo.c.raid_monster_hp != 0
            )
        )
        return query

    def update_contest_enemy_guild(self, guild_uid, enemy_guild_uid, monster, element, hp, level, count):
        query = update(self.tguildinfo).values(
            contest_enemy_guild_guid = enemy_guild_uid,
            contest_monster = monster,
            contest_element = element,
            contest_monster_hp = hp,
            contest_monster_level = level,
            contest_complete_count = count
        ).where(
            self.tguildinfo.c.guild_uid == guild_uid
        )
        return query

    def update_contest_monster_hp(self, guild_uid, cur_hp):
        query = update(self.tguildinfo).values(
            contest_monster_hp = cur_hp
        ).where(
            and_(
            self.tguildinfo.c.guild_uid == guild_uid,
            self.tguildinfo.c.contest_monster_hp != 0
            )
        )
        return query

    def regen_raid_monster(self, guild_uid, element, id, hp, level, win_count):
        query = update(self.tguildinfo).values(
            raid_monster = id,
            raid_element = element,
            raid_monster_hp = hp,
            raid_monster_level = level,
            raid_complete_count = win_count
        ).where(
            self.tguildinfo.c.guild_uid == guild_uid
        )
        return query

    def regen_contest_monster(self, guild_uid, enemy_guild_uid, id, hp, level):
        query = update(self.tguildinfo).values(
            contest_enemy_guild_guid = enemy_guild_uid,
            contest_monster = id,
            contest_monster_hp = hp,
            contest_monster_level = level
        ).where(
            self.tguildinfo.c.guild_uid == guild_uid
        )
        return query

    def join_condition_change(self, guild_uid, join_type, join_level):
        query = update(self.tguildinfo).values(
            join_level = join_level,
            join_type = join_type
        ).where(
            self.tguildinfo.c.guild_uid == guild_uid
        )
        return query

    def select_random(self, guild_uid):
        query = select([self.tguildinfo]).where(
            self.tguildinfo.c.guild_uid != guild_uid and
            self.tguildinfo.c.contest_enemy_guild_guid == None
        ).order_by(
            func.rand()
        ).limit(1)
        return query
