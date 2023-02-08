# -*- coding: utf-8 -*-
from src.common.gamecommon import GAMECOMMON
from src.common.util import *
from src.protocol.webapp_pb import *
from src.tables.table_Base import RewardData


def refreshResourceTime(self):
    refresh_flag = False
    redis_info = self.cache_clone.get_user_data(self.userid, GAMECOMMON.R_USER_REFRESH_RESOURCE)
    if redis_info:
        check_time = convert_string_to_array(redis_info)
        check_idx = int((24 - self.begin.hour) / 8)
        if 2 < check_idx:
            check_idx = 0

        if 1 != check_time[check_idx]:
            refresh_flag = True
            check_time[check_idx] = 1
            self.cache.set_user_info(self.userid, GAMECOMMON.R_USER_REFRESH_RESOURCE, str(check_time))

    return refresh_flag


class ServiceResource(object):

    def _getLevel(self, grade, exp):
        calc_value = (exp / self.table.const_exp[grade] / self.table.const_info.get(GAMECOMMON.EXP_CONST).value)
        return int(pow(calc_value, 0.5) + 1)

    # 미완성된 컨텐츠 코드 - id (자원 tableid 값이 들어오는데 파싱된 gather_reward.csv에서는 찾을 수가 없음 없는 값)
    def _gather_reward_id(self, id, lv):
        try:
            return self.table.gather_reward[id][lv-1]
        except Exception as e:
            return 0

    def ResourceAreaList(self, response):
        redis_data = self.cache_clone.get_user_data(self.userid, GAMECOMMON.R_USER_TERRITORY_INFO)
        if not redis_data:
            response.result = Response.CACHE_NOT_EXIST
            return

        redis_territory = convert_string_to_dict(redis_data)
        self.wait_build_process(redis_territory)

        db_resource_collect = self.w_db['resourcecollect'].select_all(self.userid)
        for info in db_resource_collect:
            if 0 < info.resource_id:
                resourceData = response.resourcearea_list.resource_list.add()
                resourceData.idx = info.resource_idx
                resourceData.id = info.resource_id
                resourceData.lv = info.resource_lv
                resourceData.dist = info.distance
                uid_list = convert_string_to_array(info.dispatch_list)
                resourceData.dispatch_list.extend(uid_list)
                resourceData.remain_time = calc_time_to_seconds(self.begin, info.end_time)
                if 0 > resourceData.remain_time:
                    resourceData.remain_time = 0
                resourceData.process = True
                resourceData.start_time = time_diff_in_seconds(info.start_time)
                resourceData.end_time = time_diff_in_seconds(info.end_time)
                resourceData.resource_max = info.resource_max
                resourceData.move_time = info.move_time

        if refreshResourceTime(self):
            for i in range(0, GAMECOMMON.RESOURCE_REFRESH_COUNT):
                resource, level, dist = self.generate_resource()
                self.w_db['resourcedispatch'].udpate_data(
                    self.userid,
                    i + GAMECOMMON.RESOURCE_REFRESH_COUNT,
                    resource,
                    level, 
                    dist
                )

                resourceData = response.resourcearea_list.resource_list.add()
                resourceData.idx = i + GAMECOMMON.RESOURCE_REFRESH_COUNT
                resourceData.id = resource
                resourceData.lv = level
                resourceData.dist = dist
                resourceData.remain_time = 0
                resourceData.process = False

        else:
            db_resource_collect = self.w_db['resourcedispatch'].select_all(self.userid)
            for info in db_resource_collect:
                if 0 < info.resource_id:
                    resourceData = response.resourcearea_list.resource_list.add()
                    resourceData.idx = info.resource_idx
                    resourceData.id = info.resource_id
                    resourceData.lv = info.resource_lv
                    resourceData.dist = info.distance
                    resourceData.remain_time = 0
                    resourceData.process = False

        response.result = Response.SUCCESS
        return


    def ResourceDispatch(self, request, response):
        db_resource = self.w_db['resourcedispatch'].select_idx(self.userid, request.resource_dispatch.idx)
        if not db_resource:
            response.result = Response.RESOURCE_ID_EMPTY
            return

        if len(self.table.resource_area) < db_resource.resource_lv:
            response.result = Response.INVALID_RESOURCE
            return

        redis_data = self.cache_clone.get_user_data(self.userid, GAMECOMMON.R_USER_RESOURCE_SLOT)
        if not redis_data:
            response.result = Response.USER_INVALID
            return

        empty_slot = convert_string_to_array(redis_data)
        if 1 > len(empty_slot):
            response.result = Response.MAX_DISPATCH_COUNT
            return

        db_hero_list = self.w_db['heroinven'].find_item_list(self.userid, request.resource_dispatch.uids)
        if not db_hero_list:
            response.result = Response.ITEM_INVALID
            return

        if len(db_hero_list) != len(request.resource_dispatch.uids):
            response.result = Response.ITEM_INVALID
            return

        time_seconds = 0
        move_speed = 0
        max_grade = 0
        max_value = 0
        gather_sum = 0
        area_data = self.table.resource_area[db_resource.resource_lv - 1]
        for item in db_hero_list:
            if item.auid != self.userid:
                response.result = Response.ITEM_INVALID
                return

            if item.dispatch_flag:
                response.result = Response.CANT_DISPATCH_HERO
                return

            hero_data = self.table.hero.get(item.item_id, None)
            if not hero_data:
                response.result = Response.INVALID_RESOURCE
                return

            hero_level = ServiceResource._getLevel(self, hero_data.grade, item.exp)
            if hero_level < area_data.min_lv:
                response.result = Response.LEVEL_LACK
                return

            gather_data = self.table.hero_gather[hero_data.grade - 1]
            if not gather_data:
                response.result = Response.INVALID_RESOURCE
                return

            gather_sum += gather_data.gather_speed

            if max_grade < hero_data.grade:
                max_grade = hero_data.grade
                move_speed = gather_data.move_speed

            max_value += hero_level * 10

        if max_value > area_data.amount:
            max_value = area_data.amount

        move_speed = ((db_resource.distance * 1000) / move_speed) * 2
        time_seconds = (max_value / gather_sum) + move_speed
        #end_time = get_pass_time(0, 0, time_seconds)
        # TODO: 임시 테스트 코드 - 테스트 하기 쉽게 파견 보내면 5초만에 복귀 완료 가능하게 
        end_time = datetime.now() + timedelta(seconds=5)
        collect_slot = empty_slot[0]
        del empty_slot[0]

        try:
            self.w_db['resourcecollect'].udpate_data(
                self.userid, 
                collect_slot, 
                db_resource.resource_id,
                db_resource.resource_lv, 
                db_resource.distance,
                str(request.resource_dispatch.uids), 
                self.begin, 
                end_time,
                max_value, 
                move_speed / 2
            )
        except Exception as e:
            self.logger.error("update resourcecollect error : {}".format(e.message))
            response.result = Response.DB_SYSTEM_ERROR
            return

        self.w_db['resourcedispatch'].clear_data(self.userid, request.resource_dispatch.idx)
        self.w_db['heroinven'].update_dispatch(self.userid, request.resource_dispatch.uids, True)

        self.cache.set_user_info(self.userid, GAMECOMMON.R_USER_RESOURCE_SLOT, str(empty_slot))

        response.resource_dispatch.befor_idx = request.resource_dispatch.idx
        response.resource_dispatch.after_idx = collect_slot
        response.resource_dispatch.dispatch_list.extend(request.resource_dispatch.uids)
        response.resource_dispatch.remain_time = time_diff_in_seconds(end_time)
        response.result = Response.SUCCESS
        return

    def ResourceReturn(self, request, response):
        db_resource = self.w_db['resourcecollect'].select_idx(self.userid, request.resource_return.idx)
        if not db_resource:
            response.result = Response.RESOURCE_ID_EMPTY
            return

        if db_resource.end_time < self.begin:
            response.result = Response.RESOURCE_ID_EMPTY
            return

        if 1 > db_resource.resource_id:
            response.result = Response.RESOURCE_ID_EMPTY
            return

        if 1 > db_resource.move_time:
            response.result = Response.RETURNING_HERO
            return

        resource_max = 0
        spend_time = time_diff_in_seconds(db_resource.start_time)
        return_time = db_resource.move_time

        if spend_time < db_resource.move_time:
            return_time = spend_time

        cur_second = calc_time_to_seconds(db_resource.start_time, self.begin) - db_resource.move_time
        rest_second = time_diff_in_seconds(db_resource.end_time) - (db_resource.move_time)
        collect_second = calc_time_to_seconds(db_resource.start_time, db_resource.end_time) - (db_resource.move_time * 2)
        if 1 < cur_second:
            percent = ((collect_second - rest_second) / collect_second)
            resource_max = int(db_resource.resource_max * percent)

        end_time = get_pass_time(0, 0, return_time)

        self.w_db['resourcecollect'].update_return_data(
            self.userid,
            request.resource_return.idx,
            end_time,
            resource_max
        )

        response.resource_return.idx = request.resource_return.idx
        response.resource_return.remain_time = return_time
        response.resource_return.resource_max = resource_max
        response.result = Response.SUCCESS
        return

    def ResourceReward(self, request, response):
        db_resource = self.w_db['resourcecollect'].select_idx(self.userid, request.resource_reward.idx)
        if not db_resource:
            response.result = Response.RESOURCE_ID_EMPTY
            return

        # TODO: 바로 복귀 가능하게 짧게 테스트 해서 임시 주석처리
        # if db_resource.end_time > self.begin:
        #     response.result = Response.TIME_ERROR
        #     return

        response.resource_reward.idx = request.resource_reward.idx

        if db_resource.resource_max < 0:
            response.result = Response.FAILURE
            return

        item_dict = {}
        item_dict[db_resource.resource_id] = RewardData(
            db_resource.resource_id, 
            Define.ITEM_TYPE_GOODS,
            db_resource.resource_max
        )

        update_uids = convert_string_to_array(db_resource.dispatch_list)
        self.w_db['heroinven'].update_dispatch(self.userid, update_uids, False)
        self.w_db['resourcecollect'].clear_data(self.userid, db_resource.resource_idx)

        redis_data = self.cache_clone.get_user_data(self.userid, GAMECOMMON.R_USER_RESOURCE_SLOT)
        if redis_data:
            empty_slot = convert_string_to_array(redis_data)
            empty_slot.append(db_resource.resource_idx)
            self.cache.set_user_info(self.userid, GAMECOMMON.R_USER_RESOURCE_SLOT, str(empty_slot))

        # TODO: 중간에 망가진 건지 컨텐츠가 제대로 구현이 완료되지 않음. gather_reward_id() 메서드 자체가 문제 = db_resource.resource_id (나무, 돌 같은것)
        # reward_id = ServiceResource._gather_reward_id(self, db_resource.resource_id, db_resource.resource_lv) # 기존 미완료 구현 코드
        area_type = 3 # 현재 에어리어 타입 임시고정 - 에어리어 타입이 들어와야 함. db에서 저장되고 관리되어야 함
        reward_id = self.table.gather_reward[area_type][db_resource.resource_lv - 1] # 배열 인덱스므로 -1, 기대값 : reward_set 값이 나와야 정상
        item_dict = self.get_reward_list(reward_id)
        self.reward_packet_process(
            item_dict,
            response.resource_reward.reward_list
        )
        response.result = Response.SUCCESS
        return