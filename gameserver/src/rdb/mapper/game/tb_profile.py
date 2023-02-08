# -*- coding: utf-8 -*-
from sqlalchemy import insert, select, sql, update

from src.protocol.webapp_pb import Define
from src.rdb.sqlsession import Mapper


class ProfileDAO(Mapper):
    def __init__(self, metadata):
        Mapper.__init__(self, metadata)
        table_name = self.metadata.schema + '.tb_profile'
        self.tprofile = self.tables[table_name]

    def insert_profile(self, auid, equip_normal_max, equip_pvp_max, hero_max, stamina, guild_withdraw_time, raid_ticket, arena_ticket, darknest_ticket, contest_ticket, had_hero_set):
        query = insert(self.tprofile).values(
            auid = auid,
            equip_normal_inven_max = equip_normal_max,
            equip_pvp_inven_max = equip_pvp_max,
            hero_inven_max = hero_max,
            stamina_max = stamina,
            stamina_cur = stamina,
            guild_withdraw_time = guild_withdraw_time,
            guild_raid_ticket = raid_ticket,
            arena_ticket = arena_ticket,
            darknest_ticket = darknest_ticket,
            guild_contest_ticket = contest_ticket,
            had_hero_set = had_hero_set
        )
        return query

    def find_profile(self, auid):
        query = select([self.tprofile]).where(
            self.tprofile.c.auid == auid
        )
        return query

    def update_cash(self, auid, cash):
        query = update(self.tprofile).values(
            cash = cash
        ).where(
            self.tprofile.c.auid == auid
        )
        return query

    def increase_cash(self, auid, cash):
        query = update(self.tprofile).values(
            cash = self.tprofile.c.cash + cash
        ).where(
            self.tprofile.c.auid == auid
        )
        return query

    def decrease_cash(self, auid, cash):
        query = update(self.tprofile).values(
            cash = self.tprofile.c.cash - cash
        ).where(
            self.tprofile.c.auid == auid
        )
        return query

    def update_money(self, auid, money):
        query = update(self.tprofile).values(
            money = money
        ).where(
            self.tprofile.c.auid == auid
        )
        return query

    def increase_money(self, auid, money):
        query = update(self.tprofile).values(
            money = self.tprofile.c.money + money
        ).where(
            self.tprofile.c.auid == auid
        )
        return query

    def decrease_money(self, auid, money):
        query = update(self.tprofile).values(
            money = self.tprofile.c.money - money
        ).where(
            self.tprofile.c.auid == auid
        )
        return query

    def withdraw_guild(self, auid, time):
        query = update(self.tprofile).values(
            guild_uid = 0,
            guild_withdraw_time = time
        ).where(
            self.tprofile.c.auid == auid
        )
        return query

    def guild_kick(self, auid):
        query = update(self.tprofile).values(
            guild_uid = 0,
            guild_grade = Define.GUILD_GRADE_KICK
        ).where(
            self.tprofile.c.auid == auid
        )
        return query

    def guild_out(self, auid):
        query = update(self.tprofile).values(
            guild_uid = 0,
            guild_grade = 0
        ).where(
            self.tprofile.c.auid == auid
        )
        return query

    def guild_join(self, auid, guild_uid):
        query = update(self.tprofile).values(
            guild_uid = guild_uid
        ).where(
            self.tprofile.c.auid == auid
        )
        return query

    def update_avatar_id(self, auid, avatar_id):
        query = update(self.tprofile).values(
            avatar_id = avatar_id
        ).where(
            self.tprofile.c.auid == auid
        )
        return query

    def extend_hero_inven(self, auid, inven_max, cash):
        query = update(self.tprofile).values(
            hero_inven_max = inven_max,
            cash = cash
        ).where(
            self.tprofile.c.auid == auid
        )
        return query

    def extend_equip_normal_inven(self, auid, inven_max, cash):
        query = update(self.tprofile).values(
            equip_normal_inven_max = inven_max,
            cash = cash
        ).where(
            self.tprofile.c.auid == auid
        )
        return query

    def extend_equip_pvp_inven(self, auid, inven_max, cash):
        query = update(self.tprofile).values(
            equip_pvp_inven_max = inven_max,
            cash = cash
        ).where(
            self.tprofile.c.auid == auid
        )
        return query

    # TODO: 서버코드 리팩토링2: 이렇게 불분명한 메서드 명으로 안에서 분기처리해서 퉁치는 메서드는 별로 좋지 않음.
    # 목적에 맞게 티켓별로 메서드를 명확히 하여 하나의 메서드에는 하나의 기능만 처리하게 하는게 좋다.
    def charge_amount_value(self, auid, charge_type, count, cash):
        if charge_type == Define.CHARGE_TYPE_GUILD_RAID_TICKET:
            query = update(self.tprofile).values(
                guild_raid_ticket = count,
                cash = cash
            ).where(
                self.tprofile.c.auid == auid
            )
        elif charge_type == Define.CHARGE_TYPE_ARENA_MATCH_REFRESH:
            query = update(self.tprofile).values(
                arena_match_refresh_time = sql.null(),
                cash = cash
            ).where(
                self.tprofile.c.auid == auid
            )
        elif charge_type == Define.CHARGE_TYPE_ARENA_TICKET:
            query = update(self.tprofile).values(
                arena_ticket = count,
                cash = cash
            ).where(
                self.tprofile.c.auid == auid
            )
        elif charge_type == Define.CHARGE_TYPE_DARKNEST_TICKET:
            query = update(self.tprofile).values(
                darknest_ticket = count,
                cash = cash
            ).where(
                self.tprofile.c.auid == auid
            )
        elif charge_type == Define.CHARGE_TYPE_GUILD_CONTEST_TICKET:
            query = update(self.tprofile).values(
                guild_contest_ticket = count,
                cash = cash
            ).where(
                self.tprofile.c.auid == auid
            )
        else:
            query = update(self.tprofile).values(
                stamina_cur = count,
                cash = cash
            ).where(
                self.tprofile.c.auid == auid
            )
        return query

    def update_arena_match_refresh_time(self, auid, time):
        query = update(self.tprofile).values(
            arena_match_refresh_time = time
        ).where(
            self.tprofile.c.auid == auid
        )
        return query

    def update_had_hero_set(self, auid, had_hero_set):
        query = update(self.tprofile).values(
            had_hero_set = had_hero_set
        ).where(
            self.tprofile.c.auid == auid
        )
        return query

    def update_collection_single_set(self, auid, single):
        query = update(self.tprofile).values(
            collected_single_set = single
        ).where(
            self.tprofile.c.auid == auid
        )
        return query

    def update_collection_group_set(self, auid, group):
        query = update(self.tprofile).values(
            collected_group_set = group
        ).where(
            self.tprofile.c.auid == auid
        )
        return query

    def charge_guild_contest_ticket(self):
        query = update(self.tprofile).values(
            guild_contest_ticket = 3
        )
        return query

    def update_level_set(self, auid, level_set):
        query = update(self.tprofile).values(
            level_set = level_set
        ).where(
            self.tprofile.c.auid == auid
        )
        return query

    def increase_stamina_max(self, auid, stamina_max):
        query = update(self.tprofile).values(
            stamina_cur = self.tprofile.c.stamina_cur + stamina_max,
            stamina_max = stamina_max
        ).where(
            self.tprofile.c.auid == auid
        )
        return query

    def update_last_mode(self, auid, mode):
        query = update(self.tprofile).values(
            last_mode = mode
        ).where(
            self.tprofile.c.auid == auid
        )
        return query
