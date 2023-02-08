# -*- coding: utf-8 -*-
from src.rdb.repo.repository import RepositoryBase


class ResourceCollect(RepositoryBase):
    def insert_data(self, auid, idx, time):
        session = self.game_factory.session(auid)
        with session:
            session.insert("ResourceCollectDAO.insert_data", auid, idx, time)

    def select_all(self, auid):
        session = self.game_factory.session(auid)
        with session:
            return session.query_for_all("ResourceCollectDAO.select_all", auid)

    def udpate_data(self, auid, idx, resource_id, lv, dist, dispatch_list, start_time, end_time, resource_max, move_time):
        session = self.game_factory.session(auid)
        with session:
            return session.update(
                "ResourceCollectDAO.udpate_data",
                auid,
                idx,
                resource_id,
                lv,
                dist,
                dispatch_list,
                start_time,
                end_time,
                resource_max,
                move_time
            )

    def select_idx(self, auid, idx):
        session = self.game_factory.session(auid)
        with session:
            return session.query_for_one("ResourceCollectDAO.select_idx", auid, idx)

    def update_return_data(self, auid, idx, end_time, resource_max):
        session = self.game_factory.session(auid)
        with session:
            return session.update("ResourceCollectDAO.update_return_data", auid, idx, end_time, resource_max)

    def clear_data(self, auid, idx):
        session = self.game_factory.session(auid)
        with session:
            return session.update("ResourceCollectDAO.clear_data", auid, idx)




class ResourceDispatch(RepositoryBase):
    def insert_data(self, auid, idx, id, level, dist):
        session = self.game_factory.session(auid)
        with session:
            session.insert("ResourceDispatchDAO.insert_data", auid, idx, id, level, dist)

    def select_all(self, auid):
        session = self.game_factory.session(auid)
        with session:
            return session.query_for_all("ResourceDispatchDAO.select_all", auid)

    def udpate_data(self, auid, idx, id, level, dist):
        session = self.game_factory.session(auid)
        with session:
            session.update("ResourceDispatchDAO.udpate_data", auid, idx, id, level, dist)

    def select_idx(self, auid, idx):
        session = self.game_factory.session(auid)
        with session:
            return session.query_for_one("ResourceDispatchDAO.select_idx", auid, idx)

    def clear_data(self, auid, idx):
        session = self.game_factory.session(auid)
        with session:
            return session.update("ResourceDispatchDAO.clear_data", auid, idx)