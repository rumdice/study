# -*- coding: utf-8 -*-
# import os
# from src.account_rdb import create_account_factory, create_account_clone_factory
# from src.redis.redis_storage import create_session_manager, create_session_clone_manager, create_cache, \
#     create_cache_clone, create_wave_ranking_repository, create_wave_ranking_clone_repository, create_guild, \
#     create_guild_clone
# from src.rdb.repo.game.account_repo import AccountRepository
# from src.rdb.repo.game.users_repo import UserRepository
# from src.rdb.repo.game.inven_repo import HeroInvenRepository, EquipInvenRepositiry
# from src.rdb.repo.game.team_repo import TeamRepository
# from src.rdb.repo.guild.guildinfo_repo import GuildInfoRepository
# from src.rdb.repo.guild.guilds_repo import GuildsRepository
# from src.rdb.repo.game.stageinfo_repo import StageInfoRepository
# from src.rdb.repo.game.actinfo_repo import ActInfoRepository
#
# from src.user_rdb import create_user_factory, create_user_clone_factory
#
# __author__ = 'hohyun'
#
#
# class SchedulerContext(object):
#     def __init__(self, inifile, *args, **Fkwargs):
#         from src.common.config_parser import ConfigParser
#
#         _args = args  # pylint: disable=unused-variable
#         parser = ConfigParser(basedir=os.path.dirname(inifile))
#         parser.read(inifile)
#
#         _creator = (lambda obj: obj(parser) if obj is not None else None)
#
#         self.gamedata = _creator(kwargs.pop('gamedata', None))
#         self.session_manager = create_session_manager(parser)
#         self.session_clone_manager = create_session_clone_manager(parser)
#
#         self.cache = create_cache(parser)
#         self.cache_clone = create_cache_clone(parser)
#
#         # self.ranking_repository = create_ranking_repository(parser)
#         # self.ranking_clone_repository = create_ranking_clone_repository(parser)
#
#         self.guild = create_guild(parser)
#         self.guild_clone = create_guild_clone(parser)
#
#         after_init = kwargs.pop("after_init", None)
#         if after_init is not None:
#             after_init(self, parser)
#
#
# class RepositoryFactory(object):
#     def __init__(self, parser, gamedata, write_db=False):
#
#         if write_db:
#             self.account_factory = create_account_factory(parser)
#             self.user_factory = create_user_factory(parser)
#
#         else:
#             self.account_factory = create_account_clone_factory(parser)
#             self.user_factory = create_user_clone_factory(parser)
#
#         self.gamedata = gamedata
#         self.repositories = self._get_repositories()
#
#     def __getitem__(self, item):
#         repo = self.repositories[item]
#
#         if not repo:
#             return None
#         return repo(self.account_factory, self.user_factory, self.gamedata)
#
#     def _get_repositories(self):
#         return dict(account=AccountRepository,
#                     users=UserRepository,
#                     heroinven=HeroInvenRepository,
#                     equipinven=EquipInvenRepositiry,
#                     team=TeamRepository,
#                     guildinfo=GuildInfoRepository,
#                     guild=GuildsRepository,
#                     stageinfo=StageInfoRepository,
#                     actinfo=ActInfoRepository
#                     )
#
#
# def init_callback(ctx, parser):
#     gamedata = ctx.gamedata
#     ctx.w_db = RepositoryFactory(parser, gamedata, True)
#     ctx.r_db = RepositoryFactory(parser, gamedata)
#
#
# if __name__ == '__main__':
#     context = SchedulerContext(
#         inifile="../../conf/service_local.ini",
#         after_init=init_callback
#     )
