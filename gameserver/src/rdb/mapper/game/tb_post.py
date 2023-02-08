# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import and_, delete, func, insert, select, update

from src.rdb.sqlsession import Mapper


class PostDAO(Mapper):
    def __init__(self, metadata):
        Mapper.__init__(self, metadata)
        table_name = self.metadata.schema + '.tb_post'
        self.tpost = self.tables[table_name]

    def send_post(self, auid, post_type, title_msg, post_msg, post_item, remove_time, keep_day):
        query = insert(self.tpost).values(
            auid = auid,
            post_type = post_type,
            title_msg = title_msg,
            post_msg = post_msg,
            post_item = post_item,
            remove_time = remove_time,
            keep_day = keep_day
        )
        return query

    def post_count(self, auid):
        query = select([func.count(self.tpost.c.auid)]).where(
            and_(
            self.tpost.c.auid == auid,
            self.tpost.c.read_flag == False,
            self.tpost.c.remove_time > datetime.now()
            )
        )
        return query

    def get_post_list(self, auid):
        query = select([self.tpost]).where(
            self.tpost.c.auid == auid
        )
        return query

    def get_post_with_title(self, auid, title):
        query = select([self.tpost]).where(
            and_(
            self.tpost.c.auid == auid,
            self.tpost.c.title_msg == title,
            self.tpost.c.remove_time > datetime.now()
            )
        )
        return query

    def remove_post(self, uids):
        query = delete(self.tpost).where(
            self.tpost.c.post_uid.in_(uids)
        )
        return query

    def receive_post(self, uid):
        query = update(self.tpost).values(
            read_flag = True
        ).where(
            self.tpost.c.post_uid==uid
        )
        return query

    def get_post_uids(self, uids):
        query = select([self.tpost]).where(
            self.tpost.c.post_uid.in_(uids)
        )
        return query

    def reward_post_uids(self, uids):
        query = update(self.tpost).values(
            read_flag = True,
            reward_flag = True
        ).where(
            self.tpost.c.post_uid.in_(uids)
        )
        return query
