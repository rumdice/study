# -*- coding: utf-8 -*-
from src.common.gamecommon import GAMECOMMON
from src.common.util import *
from src.protocol.webapp_pb import *


def newAttendanceInfo(self, keep_minute, event_list):
    db_attend_info = self.w_db['attendance'].get_attendance_info(self.userid)
    if not db_attend_info:
        return Response.SUCCESS

    cur_time = datetime(self.begin.year, self.begin.month, self.begin.day)
    end_event_time = self.begin
    event_cnt = 0
    reward_flag = True
    if not db_attend_info.event_end_date:
        end_event_time =  cur_time + timedelta(minutes=keep_minute)
        event_cnt = 0
        reward_flag = False
        reward_date = cur_time + timedelta(days=-1)
        self.w_db['attendance'].event_attendance_end(self.userid, reward_date, end_event_time)
    else:
        end_event_time = db_attend_info.event_end_date
        event_cnt = db_attend_info.event_attend
        if db_attend_info.event_reward_date.month != self.begin.month or db_attend_info.event_reward_date.day != self.begin.day:
            reward_flag = False

    if end_event_time < self.begin:
        return Response.SUCCESS

    event_info = event_list.add()
    event_info.event_type = Define.EVENT_TYPE_SPECIAL_ATTEND
    event_info.remain_time = time_diff_in_seconds(end_event_time)
    event_info.reward_flag = reward_flag
    event_info.param1 = event_cnt
    return Response.SUCCESS


def newAttendanceReward(self, rewardItem):
    db_attend_info = self.w_db['attendance'].get_attendance_info(self.userid)
    if not db_attend_info:
        return Response.USER_INVALID

    cur_time = datetime(self.begin.year, self.begin.month, self.begin.day)
    if db_attend_info.event_end_date <= cur_time:
        return Response.CAN_NOT_GET_DUPLICATE

    if db_attend_info.event_reward_date >= cur_time:
        return Response.CAN_NOT_GET_DUPLICATE

    table_data = self.table.event_controller[Define.EVENT_TYPE_SPECIAL_ATTEND].eventTable
    reward_attendance = db_attend_info.event_attend + 1

    if len(table_data) < reward_attendance:
        return Response.CAN_NOT_GET_DUPLICATE

    item_dict = self.get_reward_list(table_data[reward_attendance])
    self.reward_packet_process(
        item_dict,
        rewardItem
    )
    self.w_db['attendance'].event_reward_attendance(self.userid, db_attend_info.event_attend+1, cur_time)
    return Response.SUCCESS


class ServiceEvent(object):
    def EventList(self, response):
        for key, value in self.table.event_controller.items():
            if key == Define.EVENT_TYPE_SPECIAL_ATTEND:
                result = newAttendanceInfo(self, value.keep_time, response.event_list.events)
                if result != Response.SUCCESS:
                    self.logger.error("EVENT_LIST Error : Type[{}] result[{}]".format(key, result))
                    continue

        response.result = Response.SUCCESS
        return

    def EventReward(self, request, response):
        response.event_reward.event_type = request.event_reward.event_type
        if request.event_reward.event_type == Define.EVENT_TYPE_SPECIAL_ATTEND:
            response.result = newAttendanceReward(self, response.event_reward.reward_item)
            return

        response.result = Response.SUCCESS
        return