# -*- coding: utf-8 -*-
from sqlalchemy import and_, delete, func, insert, select, update

from src.rdb.sqlsession import Mapper


class ResearchDAO(Mapper):
    def __init__(self, metadata):
        Mapper.__init__(self, metadata)
        table_name = self.metadata.schema + '.tb_research'
        self.tresearch = self.tables[table_name]

    def get_research(self, auid, research_id):
        query = select([self.tresearch]).where(
            self.tresearch.c.auid == auid,
            self.tresearch.c.research_id == research_id
        )
        return query

    def get_research_status_on(self, auid):
        query = select([self.tresearch]).where(
            self.tresearch.c.auid == auid,
            self.tresearch.c.status_flag == True
        )
        return query

    def get_research_list(self, auid):
        query = select([self.tresearch]).where(
            self.tresearch.c.auid == auid
        )
        return query

    # 연구 시작시 불리는 함수 (상태값을 진행 중으로. expire_time을 완성될 시간으로 바꾼다.)
    def update_research_status(self, auid, research_id, status_flag, start_time, expire_time):
        query = update(self.tresearch).values(
            status_flag = status_flag,
            expire_time = expire_time,
            start_time = start_time
        ).where(
            and_(
            self.tresearch.c.auid == auid,
            self.tresearch.c.research_id == research_id
            )
        )
        return query

    def desc_research_step(self, auid, research_id, step):
        query = update(self.tresearch).values(
            step=self.tresearch.c.step - step
        ).where(
            and_(
            self.tresearch.c.auid == auid,
            self.tresearch.c.research_id == research_id
            )
        )
        return query

    # 클라가 연구 완료되었을때 불리는 함수 (시간은 건드리지 않고 플레그 값만 끈다)
    def update_research_finish(self, auid, research_id, status_flag):
        query = update(self.tresearch).values(
            status_flag = status_flag,
        ).where(
            and_(
            self.tresearch.c.auid == auid,
            self.tresearch.c.research_id == research_id
            )
        )
        return query

    def get_research_list_with_ids(self, auid, research_ids):
        query = select([self.tresearch]).where(
            self.tresearch.c.auid == auid,
            self.tresearch.c.research_id.in_(research_ids)
        )
        return query
