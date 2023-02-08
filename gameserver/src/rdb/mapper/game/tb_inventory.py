# -*- coding: utf-8 -*-
from sqlalchemy import and_, delete, func, insert, select, update

from src.rdb.sqlsession import Mapper

# TODO: 서버코드 리팩토링2 클레스 설계, 구조가 잘못 잡혀서 동일코드가 중복 됨. (동일한 기능을 하는 메서드가 중복 선언.)
# repo 코드도 마찬가지.

class InvenHeroDAO(Mapper):
    def __init__(self, metadata):
        Mapper.__init__(self, metadata)
        table_name = self.metadata.schema + '.tb_inven_hero'
        self.tinvenhero = self.tables[table_name]

    def insert_hero(self, auid, heroid):
        query = insert(self.tinvenhero).values(
            auid = auid,
            item_id = heroid
        )
        return query

    def select_all_item(self, auid):
        query = select([self.tinvenhero]).where(
            self.tinvenhero.c.auid == auid
        )
        return query

    def find_item(self, item_uid):
        query = select([self.tinvenhero]).where(
            self.tinvenhero.c.uid == item_uid
        )
        return query

    def del_item_list(self, uids):
        query = delete(self.tinvenhero).where(
            self.tinvenhero.c.uid.in_(uids)
        )
        return query

    def del_item(self, hero_uid):
        query = delete(self.tinvenhero).where(
            self.tinvenhero.c.uid == hero_uid
        )
        return query

    def update_exp(self, hero_uid, exp):
        query = update(self.tinvenhero).values(
            exp = exp
        ).where(
            self.tinvenhero.c.uid == hero_uid
        )
        return query

    def find_item_list(self, uids):
        query = select([self.tinvenhero]).where(
            self.tinvenhero.c.uid.in_(uids)
        )
        return query

    def update_dispatch(self, uids, flag):
        query = update(self.tinvenhero).values(
            dispatch_flag = flag
        ).where(
            self.tinvenhero.c.uid.in_(uids)
        )
        return query

    def hero_promotion(self, uid, tier):
        query = update(self.tinvenhero).values(
            tier = tier
        ).where(
            self.tinvenhero.c.uid == uid
        )
        return query

    def update_lock(self, uid, flag):
        query = update(self.tinvenhero).values(
            lock_flag = flag
        ).where(
            self.tinvenhero.c.uid == uid
        )
        return query

    def get_hero_count(self, auid):
        query = select([func.count(self.tinvenhero.c.uid)]).where(
            self.tinvenhero.c.auid == auid
        )
        return query

    # TODO: 최적화
    def update_hero_passive_skill_id1(self, hero_uid, skill_id):
        query = update(self.tinvenhero).values(
            passive_skill_id1 = skill_id
        ).where(
            self.tinvenhero.c.uid == hero_uid
        )
        return query

    def update_hero_passive_skill_id2(self, hero_uid, skill_id):
        query = update(self.tinvenhero).values(
            passive_skill_id2 = skill_id
        ).where(
            self.tinvenhero.c.uid == hero_uid
        )
        return query

    def update_hero_potential(self, hero_uid, potential_list):
        query = update(self.tinvenhero).values(
            potential_stat_list = potential_list
        ).where(
            self.tinvenhero.c.uid == hero_uid
        )
        return query

    # TODO: 최적화
    def update_hero_equip_uid1(self, hero_uid, equip_uid):
        query = update(self.tinvenhero).values(
            equip_uid1 = equip_uid
        ).where(
            self.tinvenhero.c.uid == hero_uid
        )
        return query

    def update_hero_equip_uid2(self, hero_uid, equip_uid):
        query = update(self.tinvenhero).values(
            equip_uid2 = equip_uid
        ).where(
            self.tinvenhero.c.uid == hero_uid
        )
        return query


class InvenEquipDAO(Mapper):
    def __init__(self, metadata):
        Mapper.__init__(self, metadata)
        table_name = self.metadata.schema + '.tb_inven_equip'
        self.tinvenequip = self.tables[table_name]

    def insert_equip(self, auid, itemid, type):
        query = insert(self.tinvenequip).values(
            auid = auid,
            item_id = itemid,
            inven_type = type
        )
        return query

    def select_all_item(self, userid):
        query = select([self.tinvenequip]).where(
            self.tinvenequip.c.auid == userid
        )
        return query

    def find_item(self, item_uid):
        query = select([self.tinvenequip]).where(
            self.tinvenequip.c.uid == item_uid
        )
        return query

    def find_item_list(self, uids):
        query = select([self.tinvenequip]).where(
            self.tinvenequip.c.uid.in_(uids)
        )
        return query

    def update_exp(self, equip_uid, exp):
        query = update(self.tinvenequip).values(
            exp = exp
        ).where(
            self.tinvenequip.c.uid == equip_uid
        )
        return query

    def update_lock(self, uid, flag):
        query = update(self.tinvenequip).values(
            lock_flag = flag
        ).where(
            self.tinvenequip.c.uid == uid
        )
        return query

    def del_item_list(self, uids):
        query = delete(self.tinvenequip).where(
            self.tinvenequip.c.uid.in_(uids)
        )
        return query



class InvenEtcDAO(Mapper):
    def __init__(self, metadata):
        Mapper.__init__(self, metadata)
        table_name = self.metadata.schema + '.tb_inven_etc'
        self.tinvenetc = self.tables[table_name]

    def select_all_item(self, userid):
        query = select([self.tinvenetc]).where(
            self.tinvenetc.c.auid == userid
        )
        return query

    def find_item_list(self, userid, item_ids):
        query = select([self.tinvenetc]).where(
            and_(
            self.tinvenetc.c.auid == userid,
            self.tinvenetc.c.item_id.in_(item_ids)
            )
        )
        return query

    def find_item(self, auid, item_id):
        query = select([self.tinvenetc]).where(
            and_(
            self.tinvenetc.c.auid == auid,
            self.tinvenetc.c.item_id == item_id
            )
        )
        return query

    def del_item_list(self, userid, item_ids):
        query = delete(self.tinvenetc).where(
            and_(
            self.tinvenetc.c.auid == userid,
            self.tinvenetc.c.item_id.in_(item_ids)
            )
        )
        return query

    def del_item(self, userid, item_id):
        query = delete(self.tinvenetc).where(
            and_(
            self.tinvenetc.c.auid == userid,
            self.tinvenetc.c.item_id == item_id
            )
        )
        return query

    def update_item_count(self, userid, item_id, count):
        query = update(self.tinvenetc).values(
            item_count = count
        ).where(
            and_(
            self.tinvenetc.c.auid == userid,
            self.tinvenetc.c.item_id == item_id
            )
        )
        return query

    def consume_item_count(self, auid, item_id, count):
        query = update(self.tinvenetc).values(
            item_count = self.tinvenetc.c.item_count - count
        ).where(
            and_(
            self.tinvenetc.c.auid == auid,
            self.tinvenetc.c.item_id == item_id
            )
        )
        return query

