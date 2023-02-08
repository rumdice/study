# -*- coding: utf-8 -*-
class _Constant(object):
    # const table define
    STAMINA_TIME = "stamina_time"
    STAMINA_MAX_BASIC = "stamina_max_basic"
    EXP_CONST_1 = "exp_const1"
    EXP_CONST_2 = "exp_const2"
    EXP_CONST_3 = "exp_const3"
    EXP_CONST_4 = "exp_const4"
    EXP_CONST = "exp_constant"
    ENCHANT_EXP_CONST = "enhance_exp"
    ENCHANT_MATERIAL_A = "material_expA"
    ENCHANT_MATERIAL_B = "material_expB"
    ENCHANT_GOLD = "enhance_gold"
    LEVELUP_GOLD = "levelup_gold"
    PROMOTION_GOLD = "promotion_gold"
    BASE_GOLD_STORAGE = "basic_gold_capacity"
    BASE_FOOD_STORAGE = "basic_food_capacity"
    BASE_IRON_STORAGE = "basic_iron_capacity"
    BASE_STONE_STORAGE = "basic_stone_capacity"
    BASE_WOOD_STORAGE = "basic_wood_capacity"
    RESOURCE_AREA_LEVEL = "collectShip_unlock"
    QUICK_MAKE_BUILDING = "gem_build"
    QUICK_MAKE_ITEM = "gem_craft"
    GUILD_MEMBER_MAX_COUNT = "guild_member_max_count"
    ARENA_REFRESH_COST = "arena_refresh_cost"
    ARENA_UNLOCK = "arena_unlock"
    DARKNEST_UNLOCK = "darknest_unlock"
    DUNGEON_UNLOCK = "dungeon_unlock"
    GUILD_UNLOCK = "guild_unlock"
    GUILD_CREATE = "guild_create"
    
    RAID_TICKET_MAX = "raid_max" # 토벌(길드레이드) 스테미너 최대값
    RAID_CHARGE_TIME = "raid_ticket_charge_time"
    
    ARENA_TICKET_MAX = "arena_ticket_limit"
    ARENA_CHARGE_TIME = "arena_ticket_charge_time"
    
    DARKNEST_TICKET_MAX = "darknest_ticket_limit"
    DARKNEST_CHARGE_TIME = "darknest_ticket_charge_time"
    
    CONTEST_TICKET_MAX = "guild_contest_limit"
    
    DEFAULT_HERO_MAX = "default_hero_max"
    EXTEND_HERO_MAX = "extend_hero_max"
    
    DEFAULT_EQUIP_NORMAL_MAX  = "default_equip_normal_max"
    EXTEND_EQUIP_NORMAL_MAX = "extend_equip_normal_max"
    
    DEFAULT_EQUIP_PVP_MAX = "default_equip_pvp_max"
    EXTEND_EQUIP_PVP_MAX = "extend_equip_pvp_max"
    
    EXTEND_HERO_INVEN_CASH = "extend_hero_inven_cash"
    EXTEND_HERO_INVEN_COUNT = "extend_hero_inven_count"
    
    EXTEND_EQUIP_NORMAL_CASH = "extend_equip_normal_cash"
    EXTEND_EQUIP_NORMAL_COUNT = "extend_equip_normal_count"
    
    EXTEND_EQUIP_PVP_CASH = "extend_equip_pvp_cash"
    EXTEND_EQUIP_PVP_COUNT = "extend_equip_pvp_count"

    STAMINA_CHARGE_CASH = "stamina_charge_cash"
    STAMINA_CHARGE_COUNT = "stamina_charge_count"

    DARKNEST_TICKET_CHARGE_CASH = "darknest_ticket_charge_cash"
    ARENA_TICKET_CHARGE_CASH = "arena_ticket_charge_cash"
    RAID_TICKET_CHARGE_CASH = "raid_ticket_charge_cash"

    EXTRACTOR_GOLD = "extractor_gold"

    TIER_1_MAX = "hero_max_lv_tier1"
    TIER_2_MAX = "hero_max_lv_tier2"
    TIER_3_MAX = "hero_max_lv_tier3"
    TIER_4_MAX = "hero_max_lv_tier4"
    TIER_5_MAX = "hero_max_lv_tier5"

    GUILD_LIMIT_COUNT = "guild_limit_count"
    GUILD_CHOICE_COUNT = "guild_choice_count"

    MIN_LENGTH_NICK_NAME = "nick_name_length_min"
    MAX_LENGTH_NICK_NAME = "nick_name_length_max"

    MIN_LENGTH_GUILD_NAME = "guild_name_length_min"
    MAX_LENGTH_GUILD_NAME = "guild_name_length_max"
    CASH_CONSUME_NICK_NAME_CHANGE = "change_nick_name_cash"

    DARKNEST_RESPAWN_TIME = "darknest_respawn_tick" # 다크네스트 리스폰 시간 (하루)
    RAID_END_HOUR = "raid_end_hour"

    ARENA_NORMAL_BATTLE_TIMEOUT = "arena_normal_battle_timeout"
    ARENA_NORMAL_REWARD_TERM = "arena_normal_reward_term"
    ARENA_NORMAL_WIN_REWARD = "arena_normal_win_reward"
    ARENA_NORMAL_LOSE_REWARD = "arena_normal_lose_reward"
    ARENA_NORMAL_AUTO_MATCHMAKING = "arena_normal_auto_matchmaking"


    # TODO 의도 파악
    TRADE_REFRESH_SECOND = 21600
    RESOURCE_REFRESH_COUNT = 5

    # profile redis
    R_USER_ID = "USER_ID"
    R_USER_NICK = "USER_NAME"
    R_USER_LAST_LOGIN = "USER_LAST_LOGIN"
    R_USER_TEAM_INFO = "USER_TEAM_INFO"
    R_USER_LEVEL = "USER_LEVEL"
    R_USER_EXP = "USER_EXP"
    R_USER_REFRESH_RESOURCE = "REFRESH_FLAG"
    R_USER_RESOURCE_SLOT = "RESOURCE_SLOT"
    R_USER_TERRITORY_INFO = "TERRITORY_INFO"
    R_USER_GUILD_UID = "GUILD_UID"
    R_USER_GUILD_GRADE = "GUILD_GRADE"
    R_USER_PVP_POINT = "PVP_POINT"
    R_USER_AVATAR_ID = "AVATAR_ID"
    R_USER_GUILD_POINT = "GUILD_POINT"
    R_USER_CHECK_UPDATE = "CHECK_UPDATE"
    R_USER_HAD_HERO_SET = "HAD_HERO_SET"
    R_USER_COLLECTED_SINGLE_SET = "COLLECTED_SINGLE_SET"
    R_USER_COLLECTED_GROUP_SET = "COLLECTED_GROUP_SET"
    R_USER_LEVEL_SET = "R_USER_LEVEL_SET"

    #guild info redis
    GUILD_NAME = "GUILD_NAME"
    GUILD_MASTER_UID = "MASTER_UID"
    GUILD_BG = "GUILD_BG"
    GUILD_EMBLEM = "GUILD_EMBLEM"
    GUILD_JOIN_TYPE = "GUILD_JOIN_TYPE"
    GUILD_JOIN_LEVEL = "GUILD_JOIN_LEVEL"
    GUILD_MEMBER_COUNT = "GUILD_COUNT"
    GUILD_POINT = "GUILD_POINT"
    GUILD_MESSAGE = "GUILD_MESSAGE"

    #guild rank redis
    GUILD_RANK = "GUILD_RANK"

    # arena redis
    ARENA_NORMAL = "ARENA_NORMAL"
    ARENA_HALL_OF_FAME = 'HALL_OF_FAME'
    ARENA_HALL_OF_FAME_LIST = "HALL_OF_FAME_LIST"
    ARENA_LAST_SEASON = "LAST_SEASON"

    # arena tournament redis
    R_TOURNAMENT_INFO = "TOURNAMENT_INFO"
    R_TOURNAMENT_END_DAY = 'TOURNAMENT_END_DAY'
    R_TOURNAMENT_ROUND_DAY = "TOURNAMENT_ROUND_DAY"
    R_TOURNAMENT_MATCH_LIST = 'GROUP_MATCH_LIST'

    # item table type
    TARGET_TABLE_HERO = 1
    TARGET_TABLE_ITEM = 3

    # table equip inven type
    EQUIP_INVEN_TYPE_NORMAL = 0

    # default_item_id
    ITEM_RUBY_ID = 60000001
    ITEM_GOLD_ID = 60000002
    ITEM_FOOD_ID = 60000003
    ITEM_STONE_ID = 60000004
    ITEM_IRON_ID = 60000005
    ITEM_WOOD_ID = 60000006
    ITEM_SUMMON = 60000008
    ITEM_RETURN_POINT = 60000009
    ITEM_ARENA_COIN = 60000010
    ITEM_HERO_EXP = 60000201
    ITEM_USER_EXP = 60000015
    ITEM_RESOURCE_LIST = [ITEM_FOOD_ID, ITEM_STONE_ID, ITEM_IRON_ID, ITEM_WOOD_ID]

    # play mode type
    PLAY_MODE_NONE = 0
    PLAY_MODE_REGION = 1
    PLAY_MODE_REGION_REWARD = 2
    PLAY_MODE_GUILD_RAID = 3
    PLAY_MODE_FARMING_TOWER = 4
    PLAY_MODE_EVENT_DUNGEON = 5
    PLAY_MODE_ARENA_NORMAL = 6
    PLAY_MODE_DARKNEST = 7
    PLAY_MODE_ENDLESS_TOWER = 8
    PLAY_MODE_GUILD_CONTEST = 9

    # check update
    UPDATE_GUILD_RAID = 1

    def __getattr__(self, item):
        raise AttributeError

    def __setattr__(self, key, value):
        raise AttributeError

GAMECOMMON = _Constant()
