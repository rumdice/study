# -*- coding: utf-8 -*-
from src.rdb.repo.repository import RepositoryBase


class Research(RepositoryBase):
    def get_research(self, auid, research_id):
        session = self.game_factory.session(auid)
        with session:
            return session.query_for_one("ResearchDAO.get_research", auid, research_id)

    # 현재 연구소 기획 및 로직상 연구중인 것은 only 1개여야 함
    def get_research_status_on(self, auid):
        session = self.game_factory.session(auid)
        with session:
            return session.query_for_one("ResearchDAO.get_research_status_on", auid)

    # 복수개의 형태면 _list
    def get_research_list(self, auid):
        session = self.game_factory.session(auid)
        with session:
            return session.query_for_all("ResearchDAO.get_research_list", auid)

    # 연구소의 연구 스텝을 진행 (테이블 자체가 연구를 1개라도 진행한 것만 insert 함)
    def step_up_research(self, auid, research_id, add_step):
        session = self.game_factory.session(auid)
        with session:
            return session.add_research_step(auid, research_id, add_step)

    # 연구소의 연구 스텝을 깎음
    def desc_research_step(self, auid, research_id, step):
        session = self.game_factory.session(auid)
        with session:
            return session.update("ResearchDAO.desc_research_step", auid, research_id, step)
    
    # 연구소의 연구 상태를 입력값으로 바꿈
    def update_research_status(self, auid, research_id, status, start_time, expire_time):
        session = self.game_factory.session(auid)
        with session:
            return session.update("ResearchDAO.update_research_status", auid, research_id, status, start_time, expire_time)

    # 연구소의 연구 상태를 입력값으로 바꿈
    def update_research_finish(self, auid, research_id, status):
        session = self.game_factory.session(auid)
        with session:
            return session.update("ResearchDAO.update_research_finish", auid, research_id, status)

    # 연구소 아이디 목록에 해당하는 유저 연구 달성 정보
    def get_research_list_with_ids(self, auid, research_ids):
        session = self.game_factory.session(auid)
        with session:
            return session.query_for_all("ResearchDAO.get_research_list_with_ids", auid, research_ids)
