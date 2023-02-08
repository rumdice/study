# -*- coding: utf-8 -*-
from src.rdb.repo.repository import RepositoryBase


class HeroInven(RepositoryBase):
    def insert_hero(self, auid, heroid):
        session = self.game_factory.session(auid)
        with session:
            ret = session.insert("InvenHeroDAO.insert_hero", auid, heroid)
            if ret is None:
                return None

            return ret.lastrowid

    def select_all_item(self, auid):
        session = self.game_factory.session(auid)
        with session:
            return session.query_for_all("InvenHeroDAO.select_all_item", auid)

    def find_item_list(self, auid, uids):
        session = self.game_factory.session(auid)
        with session:
            return session.query_for_all("InvenHeroDAO.find_item_list", uids)

    def find_item(self, userid, item_uid):
        session = self.game_factory.session(userid)
        with session:
            return session.query_for_one("InvenHeroDAO.find_item", item_uid)

    def del_item_list(self, userid, uids):
        session = self.game_factory.session(userid)
        with session:
            return session.update("InvenHeroDAO.del_item_list", uids)

    def del_item(self, userid, hero_uid):
        session = self.game_factory.session(userid)
        with session:
            return session.update("InvenHeroDAO.del_item", hero_uid)

    def update_exp(self, userid, hero_uid, exp):
        session = self.game_factory.session(userid)
        with session:
            return session.update("InvenHeroDAO.update_exp", hero_uid, exp)

    def update_dispatch(self, auid, uids, flag):
        session = self.game_factory.session(auid)
        with session:
            return session.update("InvenHeroDAO.update_dispatch", uids, flag)

    def hero_promotion(self, auid, uid, tier):
        session = self.game_factory.session(auid)
        with session:
            return session.update("InvenHeroDAO.hero_promotion", uid, tier)

    def update_lock(self, auid, uid, flag):
        session = self.game_factory.session(auid)
        with session:
            return session.update("InvenHeroDAO.update_lock", uid, flag)

    def get_hero_count(self, auid):
        session = self.game_factory.session(auid)
        with session:
            return session.query_for_value("InvenHeroDAO.get_hero_count", auid)

    def update_hero_passive_skill_id1(self, auid, hero_uid, skill_id):
        session = self.game_factory.session(auid)
        with session:
            return session.update("InvenHeroDAO.update_hero_passive_skill_id1", hero_uid, skill_id)

    def update_hero_passive_skill_id2(self, auid, hero_uid, skill_id):
        session = self.game_factory.session(auid)
        with session:
            return session.update("InvenHeroDAO.update_hero_passive_skill_id2", hero_uid, skill_id)

    def update_hero_potential(self, auid, hero_uid, potential_list):
        session = self.game_factory.session(auid)
        with session:
            return session.update("InvenHeroDAO.update_hero_potential", hero_uid, potential_list)

    def update_hero_equip_uid1(self, auid, hero_uid, equip_uid):
        session = self.game_factory.session(auid)
        with session:
            return session.update("InvenHeroDAO.update_hero_equip_uid1", hero_uid, equip_uid)

    def update_hero_equip_uid2(self, auid, hero_uid, equip_uid):
        session = self.game_factory.session(auid)
        with session:
            return session.update("InvenHeroDAO.update_hero_equip_uid2", hero_uid, equip_uid)




class EquipInven(RepositoryBase):
    def insert_equip(self, auid, itemid, type):
        session = self.game_factory.session(auid)
        with session:
            ret = session.insert("InvenEquipDAO.insert_equip", auid, itemid, type)
            if ret is None:
                return None

            return ret.lastrowid

    def select_all_item(self, userid):
        session = self.game_factory.session(userid)
        with session:
            return session.query_for_all("InvenEquipDAO.select_all_item", userid)

    def find_item_list(self, auid, uids):
        session = self.game_factory.session(auid)
        with session:
            return session.query_for_all("InvenEquipDAO.find_item_list", uids)

    def find_item(self, userid, item_uid):
        session = self.game_factory.session(userid)
        with session:
            return session.query_for_one("InvenEquipDAO.find_item", item_uid)

    def update_exp(self, userid, equip_uid, exp):
        session = self.game_factory.session(userid)
        with session:
            return session.update("InvenEquipDAO.update_exp", equip_uid, exp)

    def update_lock(self, auid, uid, flag):
        session = self.game_factory.session(auid)
        with session:
            return session.update("InvenEquipDAO.update_lock", uid, flag)

    def del_item_list(self, auid, uids):
        session = self.game_factory.session(auid)
        with session:
            return session.update("InvenEquipDAO.del_item_list", uids)



class EtcInven(RepositoryBase):
    def add_item(self, userid, item_id, add_count):
        session = self.game_factory.session(userid)
        with session:
            return session.add_item_count(userid, item_id, add_count)

    def select_all_item(self, userid):
        session = self.game_factory.session(userid)
        with session:
            return session.query_for_all("InvenEtcDAO.select_all_item", userid)

    def find_item_list(self, userid, item_ids):
        session = self.game_factory.session(userid)
        with session:
            return session.query_for_all("InvenEtcDAO.find_item_list", userid, item_ids)

    def find_item(self, auid, item_id):
        session = self.game_factory.session(auid)
        with session:
            return session.query_for_one("InvenEtcDAO.find_item", auid, item_id)

    def del_item_list(self, userid, item_ids):
        session = self.game_factory.session(userid)
        with session:
            return session.update("InvenEtcDAO.del_item_list", userid, item_ids)

    def del_item(self, userid, item_id):
        session = self.game_factory.session(userid)
        with session:
            return session.update("InvenEtcDAO.del_item", userid, item_id)

    def update_item_count(self, userid, item_id, update_count):
        session = self.game_factory.session(userid)
        with session:
            return session.update("InvenEtcDAO.update_item_count", userid, item_id, update_count)

    def consume_item_count(self, userid, item_id, count):
        session = self.game_factory.session(userid)
        with session:
            return session.update("InvenEtcDAO.consume_item_count", userid, item_id, count)
