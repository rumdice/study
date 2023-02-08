# -*- coding: utf-8 -*-
from src.rdb.repo.repository import RepositoryBase


class TerritoryBuild(RepositoryBase):
    def insert_territory_build(self, auid, uid, building_type, build_level, create_time):
        session = self.game_factory.session(auid)
        with session:
            session.insert(
                "TerritoryBuildDAO.insert_territory_build",
                auid,
                uid,
                building_type,
                build_level,
                create_time
            )

            # session.insert_update_territory_build(
            #     auid,
            #     uid,
            #     building_type,
            #     build_level,
            #     create_time
            # )

    def territory_build_list(self, auid):
        session = self.game_factory.session(auid)
        with session:
            return session.query_for_all("TerritoryBuildDAO.territory_build_list", auid)

    def complete_territory_build(self, auid, uid):
        session = self.game_factory.session(auid)
        with session:
            return session.delete("TerritoryBuildDAO.complete_territory_build", uid)

    def territory_build_process(self, auid, uid):
        session = self.game_factory.session(auid)
        with session:
            return session.query_for_one("TerritoryBuildDAO.territory_build_process", uid)

    def territory_build_type(self, auid, building_type):
        session = self.game_factory.session(auid)
        with session:
            return session.query_for_one("TerritoryBuildDAO.territory_build_type", auid, building_type)

    def territory_build_create_time(self, auid, uid, create_time):
        session = self.game_factory.session(auid)
        with session:
            return session.update("TerritoryBuildDAO.territory_build_create_time", uid, create_time)

    def find_territory_build(self, auid, uid):
        session = self.game_factory.session(auid)
        with session:
            return session.query_for_one("TerritoryBuildDAO.find_territory_build", uid)


