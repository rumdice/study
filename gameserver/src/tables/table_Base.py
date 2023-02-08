# -*- coding: utf-8 -*-
from src.common.gamecommon import GAMECOMMON
from src.common.util import *
from src.tables.table_Arena import *
from src.tables.table_Attendance import *
from src.tables.table_Building import *
from src.tables.table_CollectionReward import *
from src.tables.table_Const import *
from src.tables.table_Contest import *
from src.tables.table_Darknest import *
from src.tables.table_Dungeon import *
from src.tables.table_Gacha import *
from src.tables.table_Hero import *
from src.tables.table_Item import *
from src.tables.table_LevelExp import *
from src.tables.table_Potential import *
from src.tables.table_Promotion import *
from src.tables.table_Raid import *
from src.tables.table_Recipe import *
from src.tables.table_Region import *
from src.tables.table_Research import *
from src.tables.table_Resource import *
from src.tables.table_Reward import *
from src.tables.table_Shop import *
from src.tables.table_Tower import *
from src.tables.table_Trade import *


class TableBase(object):
    def __init__(self, ini_parser=None):

        # Const
        TableConst.load(self)
        self.const_info = TableConst.get(self)
        self.const_exp = TableConst.get_exp(self)

        # 보상
        RewardSet.load(self)
        RewardProb.load(self)
        RewardGroup.load(self)
        self.reward_set = RewardSet.get(self)
        self.reward_prob = RewardProb.get(self)
        self.reward_group = RewardGroup.get(self)

        # 유저 - 출석정보
        Attendance.load_tier(self)
        Attendance.load_new(self)
        Attendance.load_event(self)
        self.tier_attendance  = Attendance.get_tier(self)
        self.event_controller = Attendance.get_event_controller(self)

        # 유저 - 레벨 경험치
        LevelExp.load(self)
        self.user_level_exp = LevelExp.get_user_level_exp(self)
        self.user_level_exp_list = LevelExp.get_user_level_exp_list(self)
        self.user_exp_level_list = LevelExp.get_user_exp_level_list(self)

        # 영웅
        Hero.load(self)
        HeroBunch.load_start(self)
        HeroBunch.load_passive_skill(self)
        HeroBunch.load_return(self)
        Promotion.load(self)
        self.hero = Hero.get(self)
        self.start_hero = HeroBunch.get_start(self)
        self.passive_skill = HeroBunch.get_passive_skill(self)
        self.return_point = HeroBunch.get_return_point(self)
        self.promotion = Promotion.get(self)

        # 잠재력
        Potential.load_info(self)
        Potential.load_class(self)
        Potential.load_unlock(self)
        self.potential_info = Potential.get_info(self)
        self.potential_class = Potential.get_class(self)
        self.potential_unlock = Potential.get_unlock(self)

        # 아이템
        Item.load(self)
        self.item = Item.get(self)

        # 가챠
        Gacha.load(self)
        self.gacha_reward = Gacha.get(self)

        # 도감 - 보상
        CollectionReward.load_group(self)
        CollectionReward.load_single(self)
        self.group_reward = CollectionReward.get_group(self)
        self.single_reward = CollectionReward.get_single(self)

        # 지역
        Region.load(self)
        Region.load_mission(self)
        self.region_list = Region.get(self)
        self.region_mission_list = Region.get_mission(self)

        # 타워
        EndlessTower.load(self)
        self.endless_tower = EndlessTower.get(self)

        FarmingTower.read_farming_tower(self)
        FarmingTower.read_gold_tower(self)
        FarmingTower.read_food_tower(self)
        FarmingTower.read_stone_tower(self)
        FarmingTower.read_iron_tower(self)
        FarmingTower.read_wood_tower(self)
        FarmingTower.read_exp_tower(self)
        self.farming_tower = FarmingTower.get(self)

        # 제작소
        Recipe.load(self)
        self.recipe = Recipe.get(self)

        # 연구소
        Research.load(self)
        self.research = Research.get(self)

        # 무역선 (미구현)
        Trade.load(self)
        Trade.load_item(self)
        self.trade_goods = Trade.get(self)
        self.trade_sell = Trade.get_item_sell(self)    # 컨텐츠 내에서 쓰이는 곳이 없음. (미구현)
        self.trade_buy = Trade.get_item_buy(self)      # 컨텐츠 내에서 쓰이는 곳이 없음. (미구현)

        # 원정채집선
        Resource.load_area(self)
        Resource.load_hero_gather(self)
        Resource.load_distance(self)
        Resource.load_gather_reward(self)
        self.resource_area = Resource.get_area(self)
        self.hero_gather = Resource.get_hero_gather(self)
        self.area_distance = Resource.get_distance(self)
        self.gather_reward = Resource.get_gather_reward(self)

        # 다크네스트
        Darknest.load_monster(self)
        Darknest.load_reward(self)
        self.darknest = Darknest.get(self)

        # 고대던전
        Dungeon.load_gimmick(self)
        Dungeon.load_reward_event_rogue_like(self)
        Dungeon.load_reward_join_condition(self)
        Dungeon.load_reward_enter_once(self)
        self.dungeon_gimmick = Dungeon.get_gimmick(self)
        self.event_rogue_like = Dungeon.get_reward_event_rogue_like(self)
        self.join_condition =  Dungeon.get_reward_join_condition(self)
        self.enter_once = Dungeon.get_reward_enter_once(self)

        # 영지 - 건설
        BuildUnlock.load(self)
        self.build_unlock = BuildUnlock.get(self)

        # 건물 정보
        BuildMaterial.load_castle(self)
        BuildMaterial.load_laboratory(self)
        BuildMaterial.load_workshop(self)
        BuildMaterial.load_trade_ship(self)
        BuildMaterial.load_altar(self)
        BuildMaterial.load_field(self)
        BuildMaterial.load_mine(self)
        BuildMaterial.load_quarry(self)
        BuildMaterial.load_lumber_mill(self)
        BuildMaterial.load_food_storage(self)
        BuildMaterial.load_iron_storage(self)
        BuildMaterial.load_stone_storage(self)
        BuildMaterial.load_wood_storage(self)
        self.build_create = BuildMaterial.get(self)

        # 길드승부
        Contest.load(self)
        Contest.load_monster(self)
        self.contest = Contest.get(self)
        self.contest_monster = Contest.get_monster(self)

        # 토벌레이드
        Raid.load_damage(self)
        Raid.load_monster(self)
        Raid.load_stat(self)
        Raid.load_reward_win(self)
        Raid.load_reward_fail(self)
        self.raid_damage = Raid.get_damage(self)
        self.raid_monster = Raid.get_monster(self)
        self.raid_const_stat = Raid.get_stat(self)
        self.raid_win_reward = Raid.get_reward_win(self)
        self.raid_fail_reward = Raid.get_reward_fail(self)

        # 아레나
        Arena.load_reward_normal(self)
        Arena.load_reward_tournament(self)
        self.arena_normal_reward = Arena.get_reward_normal(self)
        self.arena_reward_tournament = Arena.get_reward_tournament(self)  #서비스 코드에서 쓰이지 않음

        # 상점(미구현)
        Shop.load_return_point(self)
        Shop.load_arena_coin(self)
        self.shop_return_point = Shop.get_return_point(self)
        self.shop_arena_coin =  Shop.get_arena_coin(self)

    def get_reward_prob_item(self, prob_id, item_dict):
        prob_group = self.reward_prob.get(prob_id, None)
        if not prob_group:
            return

        for i in range(prob_group.loop_count):
            value = 0
            random_value = util_shop_rand(1, 10000)
            for reward_prob in prob_group.group_list:
                if random_value <= (reward_prob.group_prob+value):
                    group_reward = self.reward_group.get(reward_prob.group_id, None)
                    if not group_reward:
                        return

                    reward_idx = util_shop_rand(1, len(group_reward))
                    item_info = group_reward[reward_idx-1]

                    item_data = None
                    if item_info.table_type == GAMECOMMON.TARGET_TABLE_HERO:
                        item_data = self.hero.get(item_info.item_id, None)
                    elif item_info.table_type == GAMECOMMON.TARGET_TABLE_ITEM:
                        item_data = self.item.get(item_info.item_id, None)

                    if not item_data:
                        continue

                    reward_count = util_shop_rand(item_info.min_count, item_info.max_count)

                    total_item = item_dict.get(item_info.item_id, None)
                    if not total_item:
                        item_dict[item_info.item_id] = RewardData(item_info.item_id, item_data.item_type, reward_count)
                    else:
                        reward = item_dict[item_info.item_id]
                        reward.count += reward_count

                    break
                else:
                    value += reward_prob.group_prob

    def get_reward_item_by_group_id(self, group_id, item_dict):
        group_reward = self.reward_group.get(group_id, None)

        if not group_reward:
            return

        reward_idx = util_shop_rand(1, len(group_reward))
        item_info = group_reward[reward_idx - 1]

        item_data = None
        if item_info.table_type == GAMECOMMON.TARGET_TABLE_HERO:
            item_data = self.hero.get(item_info.item_id, None)
        elif item_info.table_type == GAMECOMMON.TARGET_TABLE_ITEM:
            item_data = self.item.get(item_info.item_id, None)

        if not item_data:
            return

        reward_count = util_shop_rand(item_info.min_count, item_info.max_count)
        total_item = item_dict.get(item_info.item_id, None)
        if not total_item:
            item_dict[item_info.item_id] = RewardData(item_info.item_id, item_data.item_type, reward_count)
        else:
            reward = item_dict[item_info.item_id]
            reward.count += reward_count
        return


    def get_reward_item_by_prob(self, prob_id, item_dict):
        prob_group = self.reward_prob.get(prob_id, None)
        if not prob_group:
            return

        for i in range(prob_group.loop_count):
            value = 0
            random_value = util_shop_rand(1, 10000)
            for reward_prob in prob_group.group_list:
                if random_value <= (reward_prob.group_prob+value):
                    self.get_reward_item_by_group_id(reward_prob.group_id, item_dict)
                    break
                else:
                    value += reward_prob.group_prob


# 게임서버 서비스에 쓰이는 클래스
class RewardData(object):
    def __init__(self, item_id, item_type, count):
        self.item_id = item_id
        self.item_type = item_type
        self.count = count