from src.common.util import load_csvfile

recipe = {}

class Recipe():
    def __init__(self, material_list, use_money, wait_sec, level):
        self.material_list = material_list
        self.use_money = use_money
        self.wait_sec = wait_sec
        self.check_lv = level

    def load(self):
        table = load_csvfile(self, "recipe")
        for row in table:
            makeItem = int(row["output"])
            material_list = {}
            level = int(row["unlock"])
            for i in range(4):
                columnStr = "material" + str(i+1)
                materialid =  int(row[columnStr])
                if 0 >= materialid:
                    break

                columnStr = "qty" + str(i+1)
                qty = int(row[columnStr])
                material_list[materialid] = qty

            Money = int(row["cost"])
            makeTime = int(row["wait_sec"])
            recipe[makeItem] = Recipe(material_list, Money, makeTime, level)

    def get(self):
        return recipe

