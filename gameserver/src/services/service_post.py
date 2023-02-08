# -*- coding: utf-8 -*-
from src.common.util import *
from src.protocol.webapp_pb import *
from src.tables.table_Base import RewardData


class ServicePost(object):
    def GetPostList(self, response):
        db_post = self.w_db['post'].get_post_list(self.userid)
        if not db_post:
            response.get_post_list.CopyFrom(Response.GetPostList())
            response.result = Response.SUCCESS
            return

        del_uids = []
        for post in db_post:
            if self.begin >= post.remove_time:
                del_uids.append(post.post_uid)
                continue

            postInfo = response.get_post_list.post_list.add()
            postInfo.post_uid = post.post_uid
            postInfo.post_type = post.post_type
            postInfo.title_msg = post.title_msg
            postInfo.post_msg = post.post_msg

            reward_items = convert_string_to_array(post.post_item)
            for item in reward_items:
                rewardItem = postInfo.items.add()
                rewardItem.item_id = item[0]
                rewardItem.count = item[1]

            postInfo.read_flag = post.read_flag
            postInfo.reward_flag = post.reward_flag
            postInfo.remove_time = time_diff_in_seconds(post.remove_time)
            postInfo.keep_day = post.keep_day

        if 0 < len(del_uids):
            self.w_db['post'].remove_post(self.userid, del_uids)

        response.result = Response.SUCCESS
        return
    
    def ReceivePost(self, request, response):
        self.w_db['post'].receive_post(self.userid, request.receive_post.post_uid)
        response.result = Response.SUCCESS
        return

    def RewardPost(self, request, response):
        db_post = self.w_db['post'].get_post_uids(self.userid, request.reward_post.post_uids)
        if not db_post:
            response.result = Response.FAILURE
            return

        del_uids = []
        reward_uids = []
        reward_dict = {}

        for post in db_post:
            if self.begin >= post.remove_time:
                del_uids.append(post.post_uid)
                continue

            if post.auid != self.userid:
                continue

            if post.reward_flag == True:
                continue

            reward_items = convert_string_to_array(post.post_item)
            for item in reward_items:
                if not reward_dict.get(item[0], None):
                    itemData = self.table.item.get(item[0], None)
                    if not itemData:
                        response.result = Response.INVALID_RESOURCE
                        return

                    reward_dict[item[0]] = RewardData(itemData.id, itemData.item_type, item[1])
                else:
                    reward_dict[item[0]].count += item[1]

            reward_uids.append(post.post_uid)

        self.reward_packet_process(
            reward_dict,
            response.reward_post.reward_item
        )
        response.reward_post.post_uids.extend(reward_uids)

        if 0 < len(reward_uids):
            self.w_db['post'].reward_post_uids(self.userid, reward_uids)

        if 0 < len(del_uids):
            self.w_db['post'].remove_post(self.userid, del_uids)

        response.result = Response.SUCCESS
        return
    
    def CleanUpPost(self, request, response):
        db_post = self.w_db['post'].get_post_list(self.userid)
        if not db_post:
            response.get_post_list.CopyFrom(Response.GetPostList())
            Response.result = Response.SUCCESS
            return

        del_uids = []
        for post in db_post:
            if self.begin >= post.remove_time:
                del_uids.append(post.post_uid)
                continue

            if post.reward_flag:
                del_uids.append(post.post_uid)
                continue

            if post.read_flag:
                reward_items = convert_string_to_array(post.post_item)
                if 0 >= len(reward_items):
                    del_uids.append(post.post_uid)

        if 0 < len(del_uids):
            self.w_db['post'].remove_post(self.userid, del_uids)

        response.clean_up_post.post_uids.extend(del_uids)
        response.result = Response.SUCCESS
        return

    def DeletePost(self, request, response):
        self.w_db['post'].remove_post(self.userid, [request.delete_post.post_uid])
        response.result = Response.SUCCESS
        return