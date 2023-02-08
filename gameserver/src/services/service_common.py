# -*- coding: utf-8 -*-
# 다른 컨텐츠 서비스 py와 달리 공용으로 쓰이는 서비스 파일
import random
from bisect import bisect_right
from datetime import timedelta

from src.common.gamecommon import GAMECOMMON
from src.common.logger import LoggerManager, register_logger
from src.common.util import *
from src.protocol.webapp_pb import Define
from src.services.service_research import *

LoggerManager.init("servicecommon")
logger = LoggerManager.getLogger()

@register_logger('service')
class ServiceCommon(object):

    item_type_stack_list = [
        Define.ITEM_TYPE_GOODS,
        Define.ITEM_TYPE_POTION,
        Define.ITEM_TYPE_MATERIAL,
        Define.ITEM_TYPE_PROMOTION,
        Define.ITEM_TYPE_EQUIP
    ]

    def __init__(self):
        self.resource_list = [
            GAMECOMMON.ITEM_FOOD_ID,
            GAMECOMMON.ITEM_IRON_ID,
            GAMECOMMON.ITEM_STONE_ID,
            GAMECOMMON.ITEM_WOOD_ID
        ]

        self.build_reward_func = {
            Define.BUILDING_TYPE_CASTLE: self.DefaultBuildingLevelUp,
            Define.BUILDING_TYPE_LABORATORY: self.DefaultBuildingLevelUp,
            Define.BUILDING_TYPE_ALTAR : self.DefaultBuildingLevelUp,
            Define.BUILDING_TYPE_TRADE_SHIP : self.BuildUidLevelUP,
            Define.BUILDING_TYPE_WORKSHOP : self.BuildUidLevelUP,
            Define.BUILDING_TYPE_FIELD: self.ResourceBuildingLevelUP,
            Define.BUILDING_TYPE_MINE: self.ResourceBuildingLevelUP,
            Define.BUILDING_TYPE_QUARRY: self.ResourceBuildingLevelUP,
            Define.BUILDING_TYPE_LUMBER_MILL: self.ResourceBuildingLevelUP,
            Define.BUILDING_TYPE_FOOD_STORAGE : self.StorageLevelUP,
            Define.BUILDING_TYPE_IRON_STORAGE : self.StorageLevelUP,
            Define.BUILDING_TYPE_STONE_STORAGE : self.StorageLevelUP,
            Define.BUILDING_TYPE_WOOD_STORAGE : self.StorageLevelUP,
        }

        self.GetItemMax = {
            GAMECOMMON.ITEM_FOOD_ID: lambda redis_data: int(redis_data[Define.BUILDING_TYPE_FOOD_STORAGE]),
            GAMECOMMON.ITEM_IRON_ID: lambda redis_data: int(redis_data[Define.BUILDING_TYPE_IRON_STORAGE]),
            GAMECOMMON.ITEM_STONE_ID: lambda redis_data: int(redis_data[Define.BUILDING_TYPE_STONE_STORAGE]),
            GAMECOMMON.ITEM_WOOD_ID: lambda redis_data: int(redis_data[Define.BUILDING_TYPE_WOOD_STORAGE])
        }

    def next_charge_second(self, cur_time, charge_secounds):
        return (cur_time + timedelta(seconds=charge_secounds) - self.begin).seconds

    def get_stamina(self, userinfo, stamina_max, increase_stamina, wirte_db=False):
        add_stamina = 0
        stamina_time = None

        stamina_charge_time = int(self.table.const_info.get(GAMECOMMON.STAMINA_TIME).value)

        if userinfo.stamina_cur < stamina_max:
            if userinfo.stamina_time:
                interval = self.begin - userinfo.stamina_time if userinfo.stamina_time else timedelta(
                    seconds=stamina_max * stamina_charge_time)
                add_stamina = interval.seconds / stamina_charge_time
                if (userinfo.stamina_cur + add_stamina) < stamina_max:
                    if (userinfo.stamina_cur + add_stamina + increase_stamina) < stamina_max:
                        add_time = timedelta(
                            seconds=interval.seconds / stamina_charge_time * stamina_charge_time)
                        stamina_time = userinfo.stamina_time + add_time
                else:
                    add_stamina = stamina_max - userinfo.stamina_cur
                    if add_stamina < 0:
                        add_stamina = 0
            else:
                stamina_time = self.begin

        if wirte_db == True and (add_stamina + increase_stamina) != 0:
            pass

        total_stamina = int(userinfo.stamina_cur + add_stamina + increase_stamina)
        return (total_stamina, stamina_time)

    def generate_resource(self):
        resource = random.randint(0, len(self.resource_list)-1)
        probVal = random.randint(1, 100)
        sumVal = 0
        resource_lv = 1
        distance = 3
        for info in self.table.resource_area:
            if (sumVal + info.prob) >= probVal:
                resource_lv = info.level
                break
            else:
                sumVal += info.prob

        probVal = random.randint(1, 100)
        sumVal = 0
        for dist in self.table.area_distance:
            if (sumVal + dist.prob) >= probVal:
                distance = random.randint(dist.min, dist.max)
                break
            else:
                sumVal += info.prob

        return self.resource_list[resource], resource_lv, distance

    def quick_Completion_Cash(self, remain_time, quick_const):
        calc_value = quick_const * remain_time
        use_cash = 0
        if 1 > calc_value:
            use_cash = 1
        else:
            use_cash = calc_value % int(calc_value)
            if 0 < use_cash:
                use_cash = int(calc_value + 1)
            else:
                use_cash = int(calc_value)

        return use_cash

    def convert_team_data_redis_to_protobuf(self, protoData, redisData):
        team_dict = convert_string_to_dict(redisData)
        protoData.formation = team_dict['formation']
        
        # 이 부분에 대한 패킷은 또 서버만 쓰는 패킷인 TeamInfo임.
        for i in range(5):
            team = team_dict.get(i)
            if team:
                hero_data = protoData.heros.add()
                hero_data.hero_id = team['hero_id']
                hero_data.exp = team['exp']
                hero_data.equip1.equip_id = team['equip1']['equip_id']
                hero_data.equip1.exp = team['equip1']['exp']
                hero_data.equip2.equip_id = team['equip2']['equip_id']
                hero_data.equip2.exp = team['equip2']['exp']

    def get_reward_list(self, reward_id):
        item_dict = {}
        reward_set = self.table.reward_set.get(reward_id, None)
        if not reward_set:
            self.logger.error("reward_set not exists : reward_id({})".format(reward_id))
            return
        for prob in reward_set:
            self.table.get_reward_item_by_prob(prob, item_dict)
        return item_dict

    def wait_build_process(self, redis_data):
        db_territory_build = self.w_db['territorybuild'].territory_build_list(self.userid)
        if not db_territory_build:
            return 0

        process_cnt = 0
        for waitBuild in db_territory_build:
            build_info_dict = self.table.build_create[waitBuild.building_type]
            if not build_info_dict:
                self.logger.error("wait_build_process build create info invalid : type[{}]".format(waitBuild.building_type))
                return 10

            build_material = build_info_dict[waitBuild.build_level]
            if not build_material:
                self.logger.error("wait_build_process build create info invalid : level[{}]".format(waitBuild.building_level))
                return 10

            remain_time = time_diff_in_seconds(waitBuild.create_time)
            # 연구소 효과 적용
            # remain_time이 1000초 라고 치면 10% 차감이면 900초 적용
            reduce_time = ReserchAffectTerritoryBuildTime(self, remain_time)
            remain_time = remain_time - reduce_time
            if build_material.build_second > remain_time:
                process_cnt += 1
                continue

            process_func = self.build_reward_func.get(waitBuild.building_type, None)
            if not process_func:
                self.logger.error("wait_build_process func invalid: type[{}]".format(waitBuild.building_type))
                return 10

            process_func(waitBuild, build_info_dict, redis_data)

        return process_cnt

#region 오직 common.py에서만 쓰이는 메서드
    def StorageLevelUP(self, dbWaitBuild, build_info_dict, redis_data):
        addStorageMax = int(redis_data[dbWaitBuild.building_type])
        
        build_material = build_info_dict[dbWaitBuild.build_level]
        if build_material:
            addStorageMax = build_material.capacity

        # 연구소 효과 적용
        # 저장량 1500 이면 10% 증가시 1500 + 150 = 1650
        add_max_storage = ReserchAffectTerritoryRewardStorageMax(self, addStorageMax)
        addStorageMax = addStorageMax + add_max_storage

        self.w_db['territory'].update_territory(self.userid, dbWaitBuild.uid, dbWaitBuild.build_level, self.begin)
        self.w_db['territorybuild'].complete_territory_build(self.userid, dbWaitBuild.uid)

        redis_data[dbWaitBuild.building_type] = addStorageMax
        self.cache.set_user_info(self.userid, GAMECOMMON.R_USER_TERRITORY_INFO, str(redis_data))
        return

    def DefaultBuildingLevelUp(self, dbWaitBuild, build_info_dict, redis_data):
        redis_data[dbWaitBuild.building_type] = dbWaitBuild.build_level
        self.w_db['territory'].update_territory(self.userid, dbWaitBuild.uid, dbWaitBuild.build_level, self.begin)
        self.w_db['territorybuild'].complete_territory_build(self.userid, dbWaitBuild.uid)
        self.cache.set_user_info(self.userid, GAMECOMMON.R_USER_TERRITORY_INFO, str(redis_data))
        return

    def BuildUidLevelUP(self, dbWaitBuild, build_info_dict, redis_data):
        level_dict = redis_data[dbWaitBuild.building_type]
        level_dict[dbWaitBuild.uid] = dbWaitBuild.build_level
        redis_data[dbWaitBuild.building_type] = level_dict
        self.w_db['territory'].update_territory(self.userid, dbWaitBuild.uid, dbWaitBuild.build_level, self.begin)
        self.w_db['territorybuild'].complete_territory_build(self.userid, dbWaitBuild.uid)
        self.cache.set_user_info(self.userid, GAMECOMMON.R_USER_TERRITORY_INFO, str(redis_data))

    def ResourceBuildingLevelUP(self, dbWaitBuild, build_info_dict, redis_data):
        build_material = build_info_dict[dbWaitBuild.build_level]
        if not build_material:
            self.w_db['territory'].update_territory(self.userid, dbWaitBuild.uid, dbWaitBuild.build_level, self.begin)
            self.w_db['territorybuild'].complete_territory_build(self.userid, dbWaitBuild.uid)
            return

        levelup_time = dbWaitBuild.create_time + timedelta(seconds=build_material.build_second)

        self.w_db['territory'].update_territory(self.userid, dbWaitBuild.uid, dbWaitBuild.build_level, levelup_time)
        self.w_db['territorybuild'].complete_territory_build(self.userid, dbWaitBuild.uid)
        return
#endregion


#region 보상 및 로깅 메서드
    # TODO: 성능개선 및 리펙토링 - 성능 저하의 주범인 재화 갱신 및 RDB 로깅 메서드 
    # 이 부분에서 로깅 하는 부분의 코드 중복 제거 방법
    # RDB에 기록한다 한들 반복문을 타면서 기록하면 안된다. - 코드 중복.
    # 모든 로직이 끝나고나서 하나의 txt 파일로 로그를 한번에 기록한다. - 패킷당 하나.
    # 반복문 안에서 로깅을 하면 하나의 패킷에 아이템 갯수 만큼 로그가 rdb에 기록된다. - db 부하가 심해짐.
    # 리팩토링3차? - 각 요소가 조금씩 다른 부분을 고려하여 로깅 시스템 재설계 필요
    # 여기에서 경험치도 올려주는데 기능 분리가 필요해 보임.

    def reward_packet_process_profile(self, item_dict, reward_list, db_update, value_list, db_profile): 
        insert_hero = set()
        for key, item in item_dict.items():
            if item.item_type in ServiceCommon.item_type_stack_list:
                if item.item_id == GAMECOMMON.ITEM_RUBY_ID:
                    update_cash = db_profile.cash + item.count
                    db_update.append('cash')
                    value_list.append(update_cash)
                elif item.item_id == GAMECOMMON.ITEM_GOLD_ID:
                    update_money = db_profile.money + item.count
                    db_update.append('money')
                    value_list.append(update_money)
                elif item.item_id == GAMECOMMON.ITEM_USER_EXP:
                    user_redis = self.cache_clone.get_user_profile(self.userid)
                    db_level = db_profile.level
                    next_level_exp = self.table.user_level_exp_list[db_level]
                    update_exp = db_profile.exp + item.count
                    next_level = db_level
                    if next_level_exp < update_exp:
                        next_level = bisect_right(self.table.user_exp_level_list, update_exp)
                        db_update.append('level')
                        value_list.append(next_level)
                        pass
                    if user_redis:
                        self.cache.set_user_info(self.userid, GAMECOMMON.R_USER_EXP, update_exp)
                        self.cache.set_user_info(self.userid, GAMECOMMON.R_USER_LEVEL, next_level)

                    db_update.append('exp')
                    value_list.append(update_exp)
                
                # 루비, 골드, 경험치 이외의 아이템 - 기타 인벤에 넣음
                else:
                    etc_item = self.w_db['etcinven'].find_item(self.userid, item.item_id)
                    if not etc_item:
                        self.w_db['etcinven'].add_item(self.userid, item.item_id, item.count)
                    else:
                        redis_data = None
                        redis_territory = None
                        etc_count = etc_item.item_count + item.count
                        if item.item_id in GAMECOMMON.ITEM_RESOURCE_LIST:
                            if not redis_data:
                                redis_data = self.cache_clone.get_user_data(self.userid, GAMECOMMON.R_USER_TERRITORY_INFO)
                            if not redis_territory:
                                redis_territory = convert_string_to_dict(redis_data)
                            storageMax = self.GetItemMax[item.item_id](redis_territory)
                            if etc_count > storageMax:
                                etc_count = storageMax
                        if 0 >= etc_count:
                            continue
                        self.w_db['etcinven'].update_item_count(self.userid, item.item_id, etc_count)

                packet_item = reward_list.add()
                packet_item.item_id = item.item_id
                packet_item.item_type = item.item_type
                packet_item.count = item.count

            # 스텍형으로 쌓이는 아이템이 아닌 영웅 아이템은 영웅 인벤에 넣음
            elif Define.ITEM_TYPE_HERO == item.item_type:
                for i in range(item.count):
                    packet_item = reward_list.add()
                    packet_item.uid = self.w_db['heroinven'].insert_hero(self.userid, item.item_id)
                    packet_item.item_id = item.item_id
                    packet_item.item_type = item.item_type
                    packet_item.count = 1
                    insert_hero.add(item.item_id)
            
            # 아무것도 아닌 아이템이면 에러 처리
            else:
                self.logger.error("Unknown item_type:{}".format(item.item_type))
                pass

        # 영웅인벤추가에 대한 부가 처리
        if insert_hero:
            db_profile = self.w_db['profile'].select_column(self.userid, "had_hero_set")
            had_hero_set = convert_string_to_set(db_profile.had_hero_set)
            result = had_hero_set | insert_hero
            had_hero_set_str = convert_set_to_string(result)
            self.w_db['profile'].update_had_hero_set(self.userid, had_hero_set_str)
            user_redis = self.cache_clone.get_user_profile(self.userid)
            if user_redis:
                self.cache.set_user_info(self.userid, GAMECOMMON.R_USER_HAD_HERO_SET, had_hero_set_str)

        return

    def reward_packet_process(self, item_dict, reward_list):
        insert_hero = set()
        update_profile = False
        update_had_hero_set = False
        db_profile = None
        db_update = []
        value_list = []
        for key, item in item_dict.items():
            if item.item_type in ServiceCommon.item_type_stack_list:
                if item.item_id == GAMECOMMON.ITEM_RUBY_ID:
                    if not db_profile:
                        update_profile = True
                        db_profile = self.w_db['profile'].select_column(self.userid, "money, cash")
                    update_cash = db_profile.cash + item.count
                    db_update.append('cash')
                    value_list.append(update_cash)
                elif item.item_id == GAMECOMMON.ITEM_GOLD_ID:
                    if not db_profile:
                        update_profile = True
                        db_profile = self.w_db['profile'].select_column(self.userid, "money, cash")
                    update_money = db_profile.money + item.count
                    db_update.append('money')
                    value_list.append(update_money)
                elif item.item_id == GAMECOMMON.ITEM_USER_EXP:
                    if not db_profile:
                        update_profile = True
                        db_profile = self.w_db['profile'].select_column(self.userid, "exp, level")
                    else:
                        db_profile = self.w_db['profile'].select_column(self.userid, "exp, level")
                    user_redis = self.cache_clone.get_user_profile(self.userid)
                    db_level = db_profile.level
                    next_level_exp = self.table.user_level_exp_list[db_level]
                    update_exp = db_profile.exp + item.count
                    next_level = db_level
                    if next_level_exp < update_exp:
                        next_level = bisect_right(self.table.user_exp_level_list, update_exp)
                        db_update.append('level')
                        value_list.append(next_level)
                        pass
                    if user_redis:
                        self.cache.set_user_info(self.userid, GAMECOMMON.R_USER_EXP, update_exp)
                        self.cache.set_user_info(self.userid, GAMECOMMON.R_USER_LEVEL, next_level)
                    db_update.append('exp')
                    value_list.append(update_exp)
                else:
                    etc_item = self.w_db['etcinven'].find_item(self.userid, item.item_id)
                    if not etc_item:
                        self.w_db['etcinven'].add_item(self.userid, item.item_id, item.count)
                    else:
                        redis_data = None
                        redis_territory = None
                        etc_count = etc_item.item_count + item.count
                        if item.item_id in GAMECOMMON.ITEM_RESOURCE_LIST:
                            if not redis_data:
                                redis_data = self.cache_clone.get_user_data(self.userid, GAMECOMMON.R_USER_TERRITORY_INFO)
                            if not redis_territory:
                                redis_territory = convert_string_to_dict(redis_data)
                            storageMax = self.GetItemMax[item.item_id](redis_territory)
                            if etc_count > storageMax:
                                etc_count = storageMax
                        if 0 >= etc_count:
                            continue
                        self.w_db['etcinven'].update_item_count(self.userid, item.item_id, etc_count)

                packet_item = reward_list.add()
                packet_item.item_id = item.item_id
                packet_item.item_type = item.item_type
                packet_item.count = item.count
            elif Define.ITEM_TYPE_HERO == item.item_type:
                for i in range(item.count):
                    packet_item = reward_list.add()
                    packet_item.uid = self.w_db['heroinven'].insert_hero(self.userid, item.item_id)
                    packet_item.item_id = item.item_id
                    packet_item.item_type = item.item_type
                    packet_item.count = 1
                    update_had_hero_set = True
                    insert_hero.add(item.item_id)
            else:
                self.logger.error("Unknown item_type:{}".format(item.item_type))
                pass

        if update_profile:
            self.w_db['profile'].update_user_column(self.userid, db_update, value_list)

        if update_had_hero_set:
            db_had_hero_set = self.w_db['profile'].select_column(self.userid, "had_hero_set")
            had_hero_set = convert_string_to_set(db_had_hero_set.had_hero_set)
            result = had_hero_set | insert_hero
            had_hero_set_str = convert_set_to_string(result)
            self.w_db['profile'].update_had_hero_set(self.userid, had_hero_set_str)

            user_redis = self.cache_clone.get_user_profile(self.userid)
            if user_redis:
                self.cache.set_user_info(self.userid, GAMECOMMON.R_USER_HAD_HERO_SET, had_hero_set_str)

        return
#endregion