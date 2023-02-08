from src.common.util import load_csvfile

item = {}

class Item():
    def __init__(self, id, type, grade, value, pvpFlag):
        self.id = id
        self.item_type = type
        self.grade = grade
        self.value = value
        self.pvp = pvpFlag

    def load(self):
        table = load_csvfile(self, "Item")
        for row in table:
            id = int(row["id"])
            item_type = int(row["type"])
            grade = int(row["grade"])
            value = int(row["value"])
            pvp = int(row["PVP"])
            item[id] = Item(id, item_type, grade, value, pvp)

    def get(self):
        return item

