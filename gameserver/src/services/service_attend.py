# -*- coding: utf-8 -*-

from src.common.gamecommon import GAMECOMMON
from src.common.util import *
from src.protocol.webapp_pb import *


class ServiceAttend(object):
    def AttendInfo(self, response):
        db = self.w_db['attendance'].get_attendance_info(self.userid)
        if not db:
            Response.result = Response.USER_INVALID
            return

        attend_cnt = 0
        reward_flag = False
        attendance_day = db.attend_reward_date.day
        attendance_month = db.attend_reward_date.month

        if (attendance_month != self.begin.month) or (attendance_day != self.begin.day):
            next_reward = db.attend_reward_date + timedelta(days = 1)
            if (next_reward.month != self.begin.month) or (next_reward.day != self.begin.day):
                attend_cnt = int((db.attend_cnt / 10) - 1)
                if 0 > attend_cnt:
                    attend_cnt = 0
                else:
                    attend_cnt *= 10
            else:
                attend_cnt = db.attend_cnt
                if 50 <= db.attend_cnt:
                    attend_cnt = 40
        else:
            reward_flag = True
            attend_cnt = db.attend_cnt

        response.attend_info.attend_cnt = attend_cnt
        response.attend_info.reward_flag = reward_flag
        response.result = Response.SUCCESS
        return


    def ContinueAttendReward(self, response):
        db = self.w_db['attendance'].get_attendance_info(self.userid)
        if not db:
            Response.result = Response.SUCCESS
            return

        attend_cnt = db.attend_cnt
        attendance_day = db.attend_reward_date.day
        attendance_month = db.attend_reward_date.month

        if (attendance_month != self.begin.month) or (attendance_day != self.begin.day):
            next_reard = db.attend_reward_date + timedelta(days=1)
            if (next_reard.month != self.begin.month) or (next_reard.day != self.begin.day):
                attend_cnt = int((attend_cnt / 10) - 1)
                if 0 > attend_cnt:
                    attend_cnt = 0
                else:
                    attend_cnt *= 10

        if 50 <= attend_cnt:
            attend_cnt = 40

        reward_iter = int((attend_cnt / 10) + 1)
        reward_index = int((attend_cnt % 10) + 1)
        reward_set = self.table.tier_attendance[reward_iter][reward_index]

        if not reward_set:
            Response.result = Response.INVALID_RESOURCE
            return

        item_dict = self.get_reward_list(reward_set)
        self.reward_packet_process(
            item_dict,
            response.attend_reward.reward_item
        )
        self.w_db['attendance'].reward_attendance(
            self.userid,
            attend_cnt + 1,
            datetime(
                year = self.begin.year,
                month = self.begin.month, 
                day = self.begin.day
            )
        )
        response.result = Response.SUCCESS
        return
