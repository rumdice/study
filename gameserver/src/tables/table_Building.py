from src.common.gamecommon import GAMECOMMON
from src.common.util import load_csvfile
from src.protocol.webapp_pb import Define

build_create_info = []
build_create_info.append(None)
def get_meterial_dict(table_start_idx, table, opt_list):

    # 초기 건물 레벨에 따라 테이블 1렙 컬럼이 있고 없음 (1 or 2)
    builds = []
    for _ in range(table_start_idx):
        builds.append(None)

    for row in table:
        material_list = {}
        money = 0

        material_item = int(row["item1_id"])
        material_count = int(row["item1_qty"])

        if 0 < material_item:
            if material_item == GAMECOMMON.ITEM_GOLD_ID:
                money = material_count
            else:
                material_list[material_item] = material_count

        material_item = int(row["item2_id"])
        material_count = int(row["item2_qty"])

        if 0 < material_item:
            if material_item == GAMECOMMON.ITEM_GOLD_ID:
                money = material_count
            else:
                material_list[material_item] = material_count

        material_item = int(row["item3_id"])
        material_count = int(row["item3_qty"])

        if 0 < material_item:
            if material_item == GAMECOMMON.ITEM_GOLD_ID:
                money = material_count
            else:
                material_list[material_item] = material_count

        material_item = int(row["item4_id"])
        material_count = int(row["item4_qty"])

        if 0 < material_item:
            if material_item == GAMECOMMON.ITEM_GOLD_ID:
                money = material_count
            else:
                material_list[material_item] = material_count

        material_item = int(row["item5_id"])
        material_count = int(row["item5_qty"])

        if 0 < material_item:
            if material_item == GAMECOMMON.ITEM_GOLD_ID:
                money = material_count
            else:
                material_list[material_item] = material_count

        build_sec = int(row["build_sec"])
        
        # 추가 리펙 대상이지만 일단 넘어감.
        # 테이블 마다 조금씩 다른 추가 옵션 컬럼명과 갯수
        # capacity 옵션은 맨 마지막
        # 추가 옵션 성격이 하드코딩인데 이전 코드 보다는 낫다.
        buff_value = 0
        if ("research_buff" in opt_list):
            buff_value = int(row["research_buff"])
        if ("craft_buff" in opt_list):
            buff_value = int(row["craft_buff"])
        if ("trade_qty" in opt_list):
            buff_value = int(row["trade_qty"])
        if ("produce" in opt_list): # 컬럼명과 자료형을 상황에 따라 바꿈 - 추가 옵션이 들어가는 자리를 맞춰야 기존 테이블 파싱과 같다.
            buff_value = float(row["produce"])

        max_qty = 0
        if ("max_qty" in opt_list):
            max_qty = int(row["max_qty"])
        
        capacity = 0
        if ("capacity" in opt_list):
            capacity = int(row["capacity"])

        builds.append(BuildMaterial(material_list, build_sec, money, 0, buff_value, max_qty, capacity))
    return builds

class BuildMaterial(object):
    def __init__(self, material_list, build_second, money, cash, produce, max_qty, capacity):
        self.material_list = material_list
        self.build_second = build_second
        self.money = money
        self.cash = cash
        self.produce = produce
        self.max_qty = max_qty
        self.capacity = capacity

    def load_castle(self):
        build_create_info.append(None)
        table = load_csvfile(self, "castle")
        build_create_info[Define.BUILDING_TYPE_CASTLE] = get_meterial_dict(2, table, [])

    def load_laboratory(self):
        build_create_info.append(None)
        table = load_csvfile(self, "laboratory")
        build_create_info[Define.BUILDING_TYPE_LABORATORY] = get_meterial_dict(1, table, ["research_buff"])

    def load_workshop(self):
        build_create_info.append(None)
        table = load_csvfile(self, "workshop")
        build_create_info[Define.BUILDING_TYPE_WORKSHOP] = get_meterial_dict(1, table, ["craft_buff"])

    def load_trade_ship(self):
        build_create_info.append(None)
        table = load_csvfile(self, "trade_ship")
        build_create_info[Define.BUILDING_TYPE_TRADE_SHIP] = get_meterial_dict(1, table, ["trade_qty"])

    def load_altar(self):
        build_create_info.append(None)
        table = load_csvfile(self, "altar")
        build_create_info[Define.BUILDING_TYPE_ALTAR] = get_meterial_dict(2, table, [])

    def load_field(self):
        build_create_info.append(None)
        table = load_csvfile(self, "field")
        build_create_info[Define.BUILDING_TYPE_FIELD] = get_meterial_dict(1, table, ["produce", "max_qty"])    

    def load_mine(self):
        build_create_info.append(None)
        table = load_csvfile(self, "mine")
        build_create_info[Define.BUILDING_TYPE_MINE] = get_meterial_dict(1, table, ["produce", "max_qty"])

    def load_quarry(self):
        build_create_info.append(None)
        table = load_csvfile(self, "quarry")
        build_create_info[Define.BUILDING_TYPE_QUARRY] = get_meterial_dict(1, table, ["produce", "max_qty"])

    def load_lumber_mill(self):
        build_create_info.append(None)
        table = load_csvfile(self, "lumber_mill")
        build_create_info[Define.BUILDING_TYPE_LUMBER_MILL] = get_meterial_dict(1, table, ["produce", "max_qty"])

    def load_food_storage(self):
        build_create_info.append(None)
        table = load_csvfile(self, "food_storage")
        build_create_info[Define.BUILDING_TYPE_FOOD_STORAGE] =  get_meterial_dict(1, table, ["capacity"])

    def load_iron_storage(self):
        build_create_info.append(None)
        table = load_csvfile(self, "iron_storage")
        build_create_info[Define.BUILDING_TYPE_IRON_STORAGE] = get_meterial_dict(1, table, ["capacity"])

    def load_stone_storage(self):
        build_create_info.append(None)
        table = load_csvfile(self, "stone_storage")
        build_create_info[Define.BUILDING_TYPE_STONE_STORAGE] = get_meterial_dict(1, table, ["capacity"])

    def load_wood_storage(self):
        build_create_info.append(None)
        table = load_csvfile(self, "wood_storage")
        build_create_info[Define.BUILDING_TYPE_WOOD_STORAGE] = get_meterial_dict(1, table, ["capacity"])

    def get(self):
        return build_create_info


build_unlock = []
class BuildUnlock(object):
    def load(self):
        build_unlock.append(None)
        table = load_csvfile(self, "build_unlock")
        for row in table:
            castle_level = int(row["castle_level"])
            laboratory = int(row["laboratory"])
            workshop = int(row["workshop"])
            trade_ship = int(row["trade_ship"])
            altar = int(row["altar"])
            field = int(row["field"])
            mine = int(row["mine"])
            quarry = int(row["quarry"])
            lumber_mill = int(row["lumber_mill"])
            food_storage = int(row["food_storage"])
            iron_storage = int(row["iron_storage"])
            stone_storage = int(row["stone_storage"])
            wood_storage = int(row["wood_storage"])

            limite_list = list(range(Define.BUILDING_TYPE_MAX))
            limite_list[Define.BUILDING_TYPE_NONE] = 0
            limite_list[Define.BUILDING_TYPE_CASTLE] = castle_level
            limite_list[Define.BUILDING_TYPE_LABORATORY] = laboratory
            limite_list[Define.BUILDING_TYPE_WORKSHOP] = workshop
            limite_list[Define.BUILDING_TYPE_TRADE_SHIP] = trade_ship
            limite_list[Define.BUILDING_TYPE_ALTAR] = altar
            limite_list[Define.BUILDING_TYPE_FIELD] = field
            limite_list[Define.BUILDING_TYPE_MINE] = mine
            limite_list[Define.BUILDING_TYPE_QUARRY] = quarry
            limite_list[Define.BUILDING_TYPE_LUMBER_MILL] = lumber_mill
            limite_list[Define.BUILDING_TYPE_FOOD_STORAGE] = food_storage
            limite_list[Define.BUILDING_TYPE_IRON_STORAGE] = iron_storage
            limite_list[Define.BUILDING_TYPE_STONE_STORAGE] = stone_storage
            limite_list[Define.BUILDING_TYPE_WOOD_STORAGE] = wood_storage

            build_unlock.append(limite_list)

    def get(self):
        return build_unlock
