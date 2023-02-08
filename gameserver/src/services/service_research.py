# -*- coding: utf-8 -*-
from src.common.gamecommon import GAMECOMMON
from src.common.util import *
from src.protocol.webapp_pb import *

# 연구소 효과 적용 메서드
# research.csv 테이블 구조가 step당 value가 동일한 구조라서 가능한 코드. 
# step당 value가 각기 다른 구조라면 mysql db 설계부터 변경되는 큰 공사가 됨.

# 건물 업그레이드 비용 감소
def ReserchAffectTerritoryBuildCost(self, before_val):
    research_id_list = [70000001, 70000002]
    return ServiceResearch._calcResearchAffectPer(self, research_id_list, before_val)

# 건물 업그레이드 시간 감소
def ReserchAffectTerritoryBuildTime(self, before_val):
    research_id_list = [70000011, 70000012]
    return ServiceResearch._calcResearchAffectPer(self, research_id_list, before_val)

# 건물 즉시 완성 비용 감소
def ReserchAffectTerritoryBuildQuickCompleteCost(self, before_val):
    research_id_list = [70000021, 70000022]
    return ServiceResearch._calcResearchAffectPer(self, research_id_list, before_val)

# 자원 창고 저장량 증가
def ReserchAffectTerritoryRewardStorageMax(self, before_val):
    research_id_list = [70001001, 70001002]
    return ServiceResearch._calcResearchAffectPer(self, research_id_list, before_val)

# 자원 생산 시설 수용량 증가
def ReserchAffectTerritoryRewardMaxQTY(self, before_val):
    research_id_list = [70001011, 70001012]
    return ServiceResearch._calcResearchAffectPer(self, research_id_list, before_val)

# 자원 생산 시설 생산량 증가 - 1분당 생산 하는 거
def ReserchAffectTerritoryRewardProduceMin(self, before_val):
    research_id_list = [70001021, 70001022]
    return ServiceResearch._calcResearchAffectPer(self, research_id_list, before_val)

# 소환제단 대기시간 감소
def ReserchAffectSummonGachaTime(self, before_val):
    research_id_list = [70010001, 70010002]
    return ServiceResearch._calcResearchAffectPer(self, research_id_list, before_val)

# 소환제단 요구비용 감소
def ReserchAffectSummonGachaCost(self, before_val):
    research_id_list = [70010011, 70010012]
    return ServiceResearch._calcResearchAffectPer(self, research_id_list, before_val)

# 장비 제작 시간 감소
def ReserchAffectMakeItemTime(self, before_val):
    research_id_list = [70011001, 70011002]
    return ServiceResearch._calcResearchAffectPer(self, research_id_list, before_val)

# 장비 제작 비용 감소
def ReserchAffectMakeItemCost(self, before_val):
    research_id_list = [70011011, 70011012]
    return ServiceResearch._calcResearchAffectPer(self, research_id_list, before_val)

# 장비 즉시제작 비용 감소
def ReserchAffectMakeQuickItemCost(self, before_val):
    research_id_list = [70011021, 70011022]
    return ServiceResearch._calcResearchAffectPer(self, research_id_list, before_val)

# 연구 요구 시간 감소
def ReserchAffectResearchTime(self, before_val):
    research_id_list = [70012001, 70012002]
    return ServiceResearch._calcResearchAffectPer(self, research_id_list, before_val)

# 연구 요구 자원 감소
def ReserchAffectResearchCost(self, before_val):
    research_id_list = [70012011, 70012012]
    return ServiceResearch._calcResearchAffectPer(self, research_id_list, before_val)


# TODO: 연구소 효과 메서드만 구현. 
# 해당 컨텐츠 버그 및 구현 완성도, 재구현 여부 확인 후 연구소 효과 적용.

# 원정채집선 채집량 증가
def ReserchAffectDispatchCollectValue(self, before_val):
    research_id_list = [70020001, 70020002]
    return ServiceResearch._calcResearchAffectPer(self, research_id_list, before_val)

# 원정채집선 채집시간 감소
def ReserchAffectDispatchCollectTime(self, before_val):
    research_id_list = [70020011, 70020012]
    return ServiceResearch._calcResearchAffectPer(self, research_id_list, before_val)

# 원정채집선 이동시간 감소
def ReserchAffectDispatchMoveTime(self, before_val):
    research_id_list = [70020021, 70020022]
    return ServiceResearch._calcResearchAffectPer(self, research_id_list, before_val)

# 원정채집선 가속 비용 감소
def ReserchAffectDispatchAccelerTime(self, before_val):
    research_id_list = [70020031, 70020032]
    return ServiceResearch._calcResearchAffectPer(self, research_id_list, before_val)

# 원정채집선 자원지 추가 - type2 (기존함수와 다름)
def ReserchAffectDispatchAreaAdd(self, before_val):
    research_id_list = [70020040]
    return 0

# 무역선 무역품 거래 비용 감소
def ReserchAffectTradeCost(self, before_val):
    research_id_list = [70030001, 70030002]
    return ServiceResearch._calcResearchAffectPer(self, research_id_list, before_val)

# 무역선 무역품 갱신 시간 감소
def ReserchAffectTradeRefreshTime(self, before_val):
    research_id_list = [70030011, 70030012]
    return ServiceResearch._calcResearchAffectPer(self, research_id_list, before_val)

# 무역선 무역품 수량 증가
def ReserchAffectTradeValue(self, before_val):
    research_id_list = [70030021, 70030022]
    return ServiceResearch._calcResearchAffectPer(self, research_id_list, before_val)

# 무역선 무역 슬롯 증가 - type2 (기존함수와 다름)
def ReserchAffectTradeSlotAdd(self, before_val):
    research_id_list = [70030030]
    return 0

class ServiceResearch(object):
    def __init__(self):
        pass

    def _maxUpStorage(self, research_id_list):
        # 자신이 가지고 있는 빌딩들에 대한 redis 정보
        redis_data = self.cache_clone.get_user_data(self.userid, GAMECOMMON.R_USER_TERRITORY_INFO)
        if not redis_data:
            # response.result = Response.USER_INVALID
            return

        redis_territory = convert_string_to_dict(redis_data)
        
        beforemax1 = int(redis_territory[Define.BUILDING_TYPE_FOOD_STORAGE])
        beforemax2 = int(redis_territory[Define.BUILDING_TYPE_IRON_STORAGE])
        beforemax3 = int(redis_territory[Define.BUILDING_TYPE_STONE_STORAGE])
        beforemax4 = int(redis_territory[Define.BUILDING_TYPE_WOOD_STORAGE])

        # 창고 저장량 연구가 총 몇 스텝인가.
        add_max_storage1 = ReserchAffectTerritoryRewardStorageMax(self, beforemax1)
        add_max_storage2 = ReserchAffectTerritoryRewardStorageMax(self, beforemax2)
        add_max_storage3 = ReserchAffectTerritoryRewardStorageMax(self, beforemax3)
        add_max_storage4 = ReserchAffectTerritoryRewardStorageMax(self, beforemax4)

        beforemax1 = beforemax1 + add_max_storage1
        beforemax2 = beforemax2 + add_max_storage2
        beforemax3 = beforemax3 + add_max_storage3
        beforemax4 = beforemax4 + add_max_storage4

        # 창고 저장량들 최대치 증가 redis 변경 적용
        redis_territory[Define.BUILDING_TYPE_FOOD_STORAGE] = beforemax1
        redis_territory[Define.BUILDING_TYPE_IRON_STORAGE] = beforemax2
        redis_territory[Define.BUILDING_TYPE_STONE_STORAGE] = beforemax3
        redis_territory[Define.BUILDING_TYPE_WOOD_STORAGE] = beforemax4

        self.cache.set_user_info(self.userid, GAMECOMMON.R_USER_TERRITORY_INFO, str(redis_territory))

    def _findListTable(_id, _step, _listTypeTable):
        return [element for element in _listTypeTable if element['research_id'] == _id and element['step'] == _step]

    def _calcResearchAffectPer(self, research_id_list, before_val):
        db_research_list = self.w_db['research'].get_research_list_with_ids(self.userid, research_id_list)
        if not db_research_list:
            return 0

        step_sum = 0
        for db_research in db_research_list:
            step_sum += db_research.step

        research_table = self.table.research
        research_row = ServiceResearch._findListTable(
            research_id_list[0], 
            db_research.step,
            research_table
        )
        
        result_per = float(research_row[0].value) * step_sum
        research_affect_after_val = round((before_val * result_per / 100.0))
        return research_affect_after_val  # 이 값을 증가할 건지 차감 할 건지는 컨텐츠 마다 다름

    def ResearchList(self, response):
        db_research_list = self.w_db['research'].get_research_list(self.userid)
        if not db_research_list:
            researchInfo = response.research_list.research_info_list.add()
            response.result = Response.SUCCESS
            return

        for db_research in db_research_list:
            researchInfo = response.research_list.research_info_list.add()
            researchInfo.research_tid = db_research.research_id
            researchInfo.research_step = db_research.step
            researchInfo.expire_time = int(convert_date_to_utc(db_research.expire_time))
            researchInfo.start_time = int(convert_date_to_utc(db_research.start_time))
            researchInfo.status_flag = bool(db_research.status_flag)

        response.result = Response.SUCCESS
        return

    def ResearchStart(self, request, response):
        req_research_tid = request.research_start.research_tid
        
        # 연구소의 연구를 시작 - db insert 만 한다.
        # 연구소의 연구가 완료가 안되도 일단 step은 1로 증가 된 상태이고 클라는 딤드처리, 다만 연구가 진행 중.
        self.w_db['research'].step_up_research(self.userid, req_research_tid, 1)
        
        # 유저가 스텝업을 한 결과 값을 가져온다 최초인 경우 0->1
        db_research = self.w_db['research'].get_research(
            self.userid,
            req_research_tid
        )

        if not db_research:
            response.result = Response.USER_INVALID
            return

        # 연구소 최대 범위를 벗어났는지 체크 (현재 구현된 연구 컨텐츠는 전부 5가 최대값, 일부 2개 연구만 3,4)
        if db_research.step > 5:
            self.w_db['research'].desc_research_step(self.userid, req_research_tid, 1) # 깎음
            response.result = Response.INVAILD_RESEARCH_STEP
            return
        
        # 연구 테이블 정보 찾기
        research_table = self.table.research
        research_row = ServiceResearch._findListTable(
            req_research_tid, 
            db_research.step,
            research_table
        )

        # 골드 차감
        cosume_gold = research_row[0].item1_qty
        # 연구소 효과 적용
        reduce_cost = ReserchAffectResearchCost(self, cosume_gold)
        cosume_gold = cosume_gold - reduce_cost
        self.w_db['profile'].decrease_money(self.userid, cosume_gold)

        # 재화 차감: 골드를 제외한 [돌, 나무, 철광석, 밀]
        consume_item_dict = {
            research_row[0].item2 : research_row[0].item2_qty,
            research_row[0].item3 : research_row[0].item3_qty,
            research_row[0].item4 : research_row[0].item4_qty,
            research_row[0].item5 : research_row[0].item5_qty,
        }

        # 연구소 효과 적용
        for item_id, item_qty in consume_item_dict.items():
            reduce_item_qty = ReserchAffectResearchCost(self, item_qty)
            item_qty = item_qty - reduce_item_qty
            consume_item_dict[item_id] = item_qty

        # 연구소 효과 적용 후 값을 다시 순회 하면서 DB Update
        for item_id, item_qty in consume_item_dict.items():
            self.w_db['etcinven'].consume_item_count(self.userid, item_id, item_qty)

        # 연구소 효과 적용
        cousume_time = research_row[0].research_sec 
        reduce_time = ReserchAffectResearchTime(self, cousume_time)
        cousume_time = cousume_time - reduce_time

        # 상태값을 연구 진행중으로
        finish_time = datetime.now() + timedelta(seconds=cousume_time)
        start_time = datetime.now()
        status_flag = 1 # 1:연구중 0:연구중 아님
        self.w_db['research'].update_research_status(self.userid, req_research_tid, status_flag, start_time, finish_time)

        # 오직 창고 저장량에 해당하는 이슈에 대한 코드 추가
        # 연구 이전에 지어진 창고들은 redis에 저장된 창고 최대 저장량이 오르지 않는 이슈
        # 창고 최대 저장량 연구를 진행할때 이미 지어진 창고들에 대하여 현재 레벨에 대한 최대 저장량을 구함.
        research_id_list = [70001001, 70001002]
        if req_research_tid in research_id_list:
            ServiceResearch._maxUpStorage(self, research_id_list)


        response.result = Response.SUCCESS
        return

    def ResearchQuickComplete(self, request, response):
        db_research = self.w_db['research'].get_research(
            self.userid,
            request.research_quick_complete.research_tid
        )

        if not db_research:
            self.w_db['research'].step_up_research(self.userid, request.research_quick_complete.research_tid, 1)

        db = self.w_db['research'].get_research(
            self.userid,
            request.research_quick_complete.research_tid
        )
            
        # 유저가 연구 진행 버튼 누르고 바로 즉시 완료 누를경우 자원의 2중 차감을 방지
        if db.status_flag == 0:
            self.w_db['research'].step_up_research(self.userid, request.research_quick_complete.research_tid, 1)

            step = db.step
            if (step + 1) > 5:
                step = 5

            # 연구 테이블 정보 찾기
            research_table = self.table.research
            research_row = ServiceResearch._findListTable(
                request.research_quick_complete.research_tid, 
                step,
                research_table
            )

            # 골드 차감
            cosume_gold = research_row[0].item1_qty
            # 연구소 효과 적용
            reduce_cost = ReserchAffectResearchCost(self, cosume_gold)
            cosume_gold = cosume_gold - reduce_cost
            self.w_db['profile'].decrease_money(self.userid, cosume_gold)

            # 재화 차감: 골드를 제외한 [돌, 나무, 철광석, 밀]
            consume_item_dict = {
                research_row[0].item2 : research_row[0].item2_qty,
                research_row[0].item3 : research_row[0].item3_qty,
                research_row[0].item4 : research_row[0].item4_qty,
                research_row[0].item5 : research_row[0].item5_qty,
            }
            
            # 연구소 효과 적용.
            for item_id, item_qty in consume_item_dict.items():
                reduce_item_qty = ReserchAffectResearchCost(self, item_qty)
                item_qty = item_qty - reduce_item_qty
                consume_item_dict[item_id] = item_qty

            # 연구소 효과 적용 후 값을 다시 순회 하면서 DB Update
            for item_id, item_qty in consume_item_dict.items():
                self.w_db['etcinven'].consume_item_count(self.userid, item_id, item_qty)


        # 유저가 스텝업을 한 결과 값을 가져온다 최초인 경우 0->1
        db_after = self.w_db['research'].get_research(
            self.userid,
            request.research_quick_complete.research_tid
        )

        # 연구소 최대 범위를 벗어났는지 체크 (현재 구현된 연구 컨텐츠는 전부 5가 최대값, 일부 2개 연구만 3,4)
        if db_after.step > 5:
            self.w_db['research'].desc_research_step(self.userid, request.research_quick_complete.research_tid, 1) # 깎음
            response.result = Response.INVAILD_RESEARCH_STEP
            return

        # 즉시완료는 보석 차감.
        # 바로 연구소 즉시완료랑 일반 연구 진행중에 연구 즉시완료 2가지 케이스 (시간기준으로 하므로 2가지 다 만족)
        remain_time = time_diff_in_seconds(db.expire_time) # 현재시간 기준으로 만료시간 까지의 시간차를 초단위로 가져옴
        use_cash = self.quick_Completion_Cash(remain_time, self.table.const_info.get(GAMECOMMON.QUICK_MAKE_BUILDING).value)
        self.w_db['profile'].decrease_cash(self.userid, use_cash)

        # 연구 일반 버튼을 누른뒤 바로 즉시완료를 누를 경우 진행 완료 상태로 바꾸어야함.
        status_flag = 0
        self.w_db['research'].update_research_finish(self.userid, request.research_quick_complete.research_tid, status_flag)

        response.result = Response.SUCCESS
        return


    def ResearchEnd(self, request, response):
        # 연구 완료된 연구를 상태를 끈다.
        status_flag = 0 # 1:연구중 0:연구중 아님
        self.w_db['research'].update_research_finish(self.userid, request.research_end.research_tid, status_flag)
        
        response.result = Response.SUCCESS
        return
