# -*- coding: utf-8 -*-
from src.rdb.repo.repository import RepositoryBase


class Profile(RepositoryBase):
    def insert_profile(self, auid, equip_normal_max, equip_pvp_max, hero_max, stamina, guild_withdraw_time, raid_ticket, arena_ticket, darknest_ticket, contest_ticket, had_hero_set):
        session = self.game_factory.session(auid)
        with session:
            session.insert(
                "ProfileDAO.insert_profile",
                auid,
                equip_normal_max,
                equip_pvp_max,
                hero_max,
                stamina,
                guild_withdraw_time,
                raid_ticket,
                arena_ticket,
                darknest_ticket,
                contest_ticket,
                had_hero_set
            )

    def find_profile(self, userid):
        session = self.game_factory.session(userid)
        with session:
            return session.query_for_one("ProfileDAO.find_profile", userid)

    def update_user_column(self, userid, column, value, str_column=None):
        session = self.game_factory.session(userid)
        with session:
            update_str = ''
            limite = len(column)
            if None != str_column:
                if 0 < limite:
                    update_str = str_column + ', '
                else:
                    update_str = str_column

            for idx, col in enumerate(column):
                if idx == (limite-1):
                    update_str += ('%s=%s') % (col, value[idx])
                else:
                    update_str += ('%s=%s, ') % (col, value[idx])

            return session.update_column_userid('tb_profile', update_str, userid)

    def select_column(self, userid, columnStr):
        session = self.game_factory.session(userid)
        with session:
            return session.select_profile_column("tb_profile", columnStr, userid)

    def update_cash(self, auid, cash):
        session = self.game_factory.session(auid)
        with session:
            return session.update("ProfileDAO.update_cash", auid, cash)

    def increase_cash(self, auid, cash):
        session = self.game_factory.session(auid)
        with session:
            return session.update("ProfileDAO.increase_cash", auid, cash)
    
    def decrease_cash(self, auid, cash):
        session = self.game_factory.session(auid)
        with session:
            return session.update("ProfileDAO.decrease_cash", auid, cash)

    def update_money(self, auid, money):
        session = self.game_factory.session(auid)
        with session:
            return session.update("ProfileDAO.update_money", auid, money)

    def increase_money(self, auid, money):
        session = self.game_factory.session(auid)
        with session:
            return session.update("ProfileDAO.increase_money", auid, money)

    def decrease_money(self, auid, money):
        session = self.game_factory.session(auid)
        with session:
            return session.update("ProfileDAO.decrease_money", auid, money)

    def withdraw_guild(self, userid, time):
        session = self.game_factory.session(userid)
        with session:
            return session.update("ProfileDAO.withdraw_guild", userid, time)

    def guild_out(self, userid):
        session = self.game_factory.session(userid)
        with session:
            return session.update("ProfileDAO.guild_out", userid)

    def guild_kick(self, userid):
        session = self.game_factory.session(userid)
        with session:
            return session.update("ProfileDAO.guild_kick", userid)

    def guild_join(self, userid, guild_uid):
        session = self.game_factory.session(userid)
        with session:
            return session.update("ProfileDAO.guild_join", userid, guild_uid)

    def update_avatar_id(self, auid, avatar_id):
        session = self.game_factory.session(auid)
        with session:
            return session.update("ProfileDAO.update_avatar_id", auid, avatar_id)

    def extend_hero_inven(self, auid, inven_max, cash):
        session = self.game_factory.session(auid)
        with session:
            return session.update("ProfileDAO.extend_hero_inven", auid, inven_max, cash)

    def extend_equip_normal_inven(self, auid, inven_max, cash):
        session = self.game_factory.session(auid)
        with session:
            return session.update("ProfileDAO.extend_equip_normal_inven", auid, inven_max, cash)

    def extend_equip_pvp_inven(self, auid, inven_max, cash):
        session = self.game_factory.session(auid)
        with session:
            return session.update("ProfileDAO.extend_equip_pvp_inven", auid, inven_max, cash)

    def charge_amount_value(self, auid, charge_type, count, cash):
        session = self.game_factory.session(auid)
        with session:
            return session.update("ProfileDAO.charge_amount_value", auid, charge_type, count, cash)

    def update_arena_match_refresh_time(self, auid, arena_match_refresh_time):
        session = self.game_factory.session(auid)
        with session:
            return session.update("ProfileDAO.update_arena_match_refresh_time", auid, arena_match_refresh_time)

    def update_had_hero_set(self, auid, had_hero_set):
        session = self.game_factory.session(auid)
        with session:
            return session.update("ProfileDAO.update_had_hero_set", auid, had_hero_set)

    def update_collection_single_set(self, auid, single):
        session = self.game_factory.session(auid)
        with session:
            return session.update("ProfileDAO.update_collection_single_set", auid, single)

    def update_collection_group_set(self, auid, group):
        session = self.game_factory.session(auid)
        with session:
            return session.update("ProfileDAO.update_collection_group_set", auid, group)

    def charge_guild_contest_ticket(self):
        session = self.game_factory.session()
        with session:
            return session.update("ProfileDAO.charge_guild_contest_ticket")

    def update_level_set(self, auid, level_set):
        session = self.game_factory.session(auid)
        with session:
            return session.update("ProfileDAO.update_level_set", auid, level_set)

    def increase_stamina_max(self, auid, stamina_max):
        session = self.game_factory.session(auid)
        with session:
            return session.update("ProfileDAO.increase_stamina_max", auid, stamina_max)

    def update_last_mode(self, auid, last_mode):
        session = self.game_factory.session(auid)
        with session:
            return session.update("ProfileDAO.update_last_mode", auid, last_mode)
