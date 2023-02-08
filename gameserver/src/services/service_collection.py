# -*- coding: utf-8 -*-
from src.common.gamecommon import GAMECOMMON
from src.common.util import *
from src.protocol.webapp_pb import *


class ServiceCollection(object):
    def CollectionInfo(self, request, response):
        response.collection_info.CopyFrom(Response.CollectionInfo())
        collected_single_str = '{}'
        collected_group_str = '{}'
        had_hero_set_str = '{}'

        user_redis = self.cache_clone.get_user_profile(self.userid)
        if user_redis:
            collected_single_str = user_redis[GAMECOMMON.R_USER_COLLECTED_SINGLE_SET]
            collected_group_str = user_redis[GAMECOMMON.R_USER_COLLECTED_GROUP_SET]
            had_hero_set_str = user_redis[GAMECOMMON.R_USER_HAD_HERO_SET]
        else:
            db_profile = self.w_db['profile'].select_column(self.userid, "collected_single_set, collected_group_set, had_hero_set")
            collected_single_str = db_profile.collected_single_set
            collected_group_str = db_profile.collected_group_set
            had_hero_set_str = db_profile.collected_group_set

        collected_single_set = convert_string_to_set(collected_single_str)
        collected_group_set = convert_string_to_set(collected_group_str)
        had_hero_set = convert_string_to_set(had_hero_set_str)

        response.collection_info.had_hero_uids.extend(list(had_hero_set))

        for value in collected_single_set:
            hero_data = self.table.hero.get(value)
            if not hero_data:
                response.result = Response.INVALID_GAMEDATA
                return
            grade = hero_data.grade

            filtered = filter(lambda x: x.grade == grade, self.table.single_reward)
            found = next(filtered, None)
            if found is None:
                response.result = Response.INVALID_GAMEDATA
                return

            item = response.collection_info.single.add()
            item.hero_uid = value
            item.grade = found.grade
            item.reward_set = found.reward_set

        for group_tuple in collected_group_set:
            grade = group_tuple[0]
            tier = group_tuple[1]
            hero_count = group_tuple[2]

            filtered = filter(lambda x: x.grade == grade and x.tier == tier and x.hero_count == hero_count, self.table.group_reward)
            found = next(filtered, None)
            if found is None:
                response.result = Response.INVALID_GAMEDATA
                return

            item = response.collection_info.group.add()
            item.grade = found.grade
            item.tier = found.tier
            item.hero_count = found.hero_count
            item.reward_set = found.reward_set

        response.result = Response.SUCCESS
        return

    def CollectionReward(self, request, response):
        user_redis = self.cache_clone.get_user_profile(self.userid)
        if not user_redis:
            response.result = Response.CACHE_NOT_EXIST
            return

        if request.collection_reward.collection_type == Define.COLLECTION_TYPE_SINGLE:
            hero_uid = request.collection_reward.single.hero_uid
            hero_data = self.table.hero.get(hero_uid)
            if not hero_data:
                response.result = Response.INVALID_GAMEDATA
                return
            grade = hero_data.grade

            filtered = filter(lambda x: x.grade == grade, self.table.single_reward)
            found = next(filtered, None)
            if found is None:
                response.result = Response.INVALID_GAMEDATA
                return

            collected_single_str = user_redis[GAMECOMMON.R_USER_COLLECTED_SINGLE_SET]
            collected_single_set = convert_string_to_set(collected_single_str)
            exists = collected_single_set and hero_uid in collected_single_set
            if exists:
                response.result = Response.INVALID_COLLECTION_CONDITION
                return

            collected_single_set.add(hero_uid)
            item_dict = self.get_reward_list(found.reward_set)
            self.reward_packet_process(
                item_dict,
                response.collection_reward.reward_item
            )

            self.cache.set_user_info(self.userid, GAMECOMMON.R_USER_COLLECTED_SINGLE_SET, convert_set_to_string(collected_single_set))
            self.w_db['profile'].update_collection_single_set(self.userid, convert_set_to_string(collected_single_set))

        elif request.collection_reward.collection_type == Define.COLLECTION_TYPE_GROUP:
            grade = request.collection_reward.group.grade
            tier = request.collection_reward.group.tier
            hero_count = request.collection_reward.group.hero_count

            filtered = filter(lambda x: x.grade == grade and x.tier == tier and x.hero_count == hero_count, self.table.group_reward)
            found = next(filtered, None)
            if found is None:
                response.result = Response.INVALID_RESOURCE
                return

            collected_group_str = user_redis[GAMECOMMON.R_USER_COLLECTED_GROUP_SET]
            group_tuple = (grade, tier, hero_count)
            collected_group_set = convert_string_to_set(collected_group_str)
            exists = collected_group_set and [item for item in collected_group_set if group_tuple == item]
            if exists:
                response.result = Response.INVALID_COLLECTION_CONDITION
                return

            collected_group_set.add(group_tuple)
            item_dict = self.get_reward_list(found.reward_set)
            self.reward_packet_process(
                item_dict,
                response.collection_reward.reward_item
            )
            self.cache.set_user_info(self.userid, GAMECOMMON.R_USER_COLLECTED_GROUP_SET, convert_set_to_string(collected_group_set))
            self.w_db['profile'].update_collection_group_set(self.userid, convert_set_to_string(collected_group_set))
        else:
            pass

        response.result = Response.SUCCESS
        return