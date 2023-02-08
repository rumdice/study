# -*- coding: utf-8 -*-
from random import randint

from src.common.gamecommon import GAMECOMMON
from src.common.util import *
from src.protocol.webapp_pb import *
from src.services.service_arena_normal import *
from src.services.service_arena_tournament import *

# TODO: 아레나 리팩토링 - 일반전, 토너먼트(재구현), 리그전(현재 미구현)
# 각자 클레스 및 파일로 분산처리

# TODO: 하드코딩 제거 방안? 초기 팀 셋팅 redis init 
# 이 부분이 레디스에 굉장히 의존적인데 설계가 엉성해서 문제가 많음. uid 관련
# 이 부분의 구조체대로 레디스에 저장된다 (hashset) (id : 테이블 id) (uid : db생성 고유 id)
def initHeroRedisData(index, addHeroSlot):
    addHeroSlot[index] = {}
    addHeroSlot[index]['hero_id'] = 0
    addHeroSlot[index]['hero_uid'] = 0
    addHeroSlot[index]['exp'] = 0
    addHeroSlot[index]['equip1'] = {}
    addHeroSlot[index]['equip1']['equip_id'] = 0
    addHeroSlot[index]['equip1']['equip_uid'] = 0
    addHeroSlot[index]['equip1']['exp'] = 0
    addHeroSlot[index]['equip2'] = {}
    addHeroSlot[index]['equip2']['equip_id'] = 0
    addHeroSlot[index]['equip2']['equip_uid'] = 0
    addHeroSlot[index]['equip2']['exp'] = 0


class ServiceArena(object):
    def __init__(self):
        self.GetInfoProc = {
            Define.ARENA_TYPE_NORMAL: ServiceArenaNormal.get_info,
            Define.ARENA_TYPE_LEAGUE: None,
            Define.ARENA_TYPE_TOURNAMENT: ServiceArenaTournament.Get_Info,
        }

        self.GetMatchProc = {
            Define.ARENA_TYPE_NORMAL: ServiceArenaNormal.get_match,
            Define.ARENA_TYPE_LEAGUE: None,
            Define.ARENA_TYPE_TOURNAMENT: ServiceArenaTournament.get_match,
        }

        self.StartBattleProc = {
            Define.ARENA_TYPE_NORMAL: ServiceArenaNormal.start_battle,
            Define.ARENA_TYPE_LEAGUE: None,
            Define.ARENA_TYPE_TOURNAMENT: ServiceArenaTournament.start_battle,
        }

        self.EndBattleProc = {
            Define.ARENA_TYPE_NORMAL: ServiceArenaNormal.end_battle,
            Define.ARENA_TYPE_LEAGUE: None,
            Define.ARENA_TYPE_TOURNAMENT: ServiceArenaTournament.end_battle,
        }

        self.RewardProc = {
            Define.ARENA_TYPE_NORMAL: ServiceArenaNormal.reward,
            Define.ARENA_TYPE_LEAGUE: None,
            Define.ARENA_TYPE_TOURNAMENT: ServiceArenaTournament.reward,
        }

        self.BattleProc = {
            Define.ARENA_TYPE_NORMAL: ServiceArenaNormal.battle_record,
            Define.ARENA_TYPE_LEAGUE: None,
            Define.ARENA_TYPE_TOURNAMENT: None,
        }

        self.RankingProc = {
            Define.ARENA_TYPE_NORMAL: ServiceArenaNormal.ranking,
            Define.ARENA_TYPE_LEAGUE: None,
            Define.ARENA_TYPE_TOURNAMENT: None,
        }

    def GetArenaInfo(self, request, response):
        self.GetInfoProc[request.get_arena_info.get_type](self, response)
        return

    def GetArenaMatchList(self, request, response):
        self.GetMatchProc[request.get_arena_match_list.get_type](self, response)
        return

    def StartArenaBattle(self, request, response):
        self.StartBattleProc[request.start_arena_battle.battle_type](self, request, response)
        return

    def EndArenaBattle(self, request, response):
        self.EndBattleProc[request.end_arena_battle.battle_type](self, request, response)
        return

    def ArenaRankingList(self, request, response):
        self.RankingProc[request.arena_ranking_list.rank_type](self, response)
        return

    def ArenaReward(self, request, response):
        self.RewardProc[request.arena_reward.arena_type](self, response)
        return

    def ArenaRecordList(self, request, response):
        self.BattleProc[request.arena_record_list.arena_type](self, response)
        return

    def UpdateTeamInfo(self, request, response):
        add_index = 0
        addHeroSlot = {}
        addHeroSlot['formation'] = request.update_team_info.formation

        for teamHero in request.update_team_info.team_hero:
            initHeroRedisData(add_index, addHeroSlot)

            # 서버 클라 패킷 설계의 미숙함으로 인한 코드.클라에서 아레나 팀 편성 관련 패킷을 쪼개서 서버의 데이터를 넣음
            if 0 < teamHero.hero_uid:
                db_hero = self.w_db['heroinven'].find_item(self.userid, teamHero.hero_uid)
                if db_hero:
                    addHeroSlot[add_index]['hero_id'] = db_hero.item_id
                    addHeroSlot[add_index]['hero_uid'] = db_hero.uid # 팀 셋팅시 고윳값을 저장해 두어야 하겠다.
                    addHeroSlot[add_index]['exp'] = db_hero.exp

            if 0 < teamHero.equip1_uid:
                db_equip = self.w_db['equipinven'].find_item(self.userid, teamHero.equip1_uid)
                if db_equip:
                    addHeroSlot[add_index]['equip1']['equip_id'] = db_equip.item_id
                    addHeroSlot[add_index]['equip1']['equip_uid'] = db_equip.uid
                    addHeroSlot[add_index]['equip1']['exp'] = db_equip.exp

            if 0 < teamHero.equip2_uid:
                db_equip = self.w_db['equipinven'].find_item(self.userid, teamHero.equip2_uid)
                if db_equip:
                    addHeroSlot[add_index]['equip2']['equip_id'] = db_equip.item_id
                    addHeroSlot[add_index]['equip2']['equip_uid'] = db_equip.uid
                    addHeroSlot[add_index]['equip2']['exp'] = db_equip.exp

            add_index += 1

        # TODO: redis team info 삭제 예정
        self.cache.set_user_info(self.userid, GAMECOMMON.R_USER_TEAM_INFO, str(addHeroSlot))
        response.result = Response.SUCCESS
        return


    def CheckEnterArena(self, response):
        db_info = self.w_db['profile'].select_column(self.userid, "arena_ticket, arena_ticket_time, level")
        if not db_info:
            response.result = Response.USER_INVALID
            return

        arena_unlock_lv = int(self.table.const_info.get(GAMECOMMON.ARENA_UNLOCK).value)
        if db_info.level < arena_unlock_lv:
            response.result = Response.CONTENT_LEVEL_LACK
            return
        
        response.result = Response.SUCCESS
        return
