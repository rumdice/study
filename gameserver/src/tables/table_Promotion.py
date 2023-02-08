from src.common.util import load_csvfile

promotion = {}

class Promotion():
    def __init__(self, list, data):
        self.material_list = list
        self.material_data = data

    def load(self):
        table = load_csvfile(self, "promotion")
        for row in table:
            group_id = int(row["group"])
            tier = int(row["tier"])
            id_list = []
            material_list = {}

            for i in range(5):
                read_str = "item"+str(i+1)
                item_id = int(row[read_str])
                if 0 >= item_id:
                    continue

                id_list.append(item_id)
                read_str = "item"+str(i+1)+"_qty"
                count = int(row[read_str])
                material_list[item_id] = count

            if not promotion.get(group_id):
                tier_list = {}
                tier_list[tier] = Promotion(id_list, material_list)
                promotion[group_id] = tier_list
            else:
                promotion[group_id][tier] = Promotion(id_list, material_list)

    def get(self):
        return promotion