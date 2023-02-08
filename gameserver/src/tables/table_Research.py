from src.common.util import load_csvfile

research_list = []

class Research(dict):
    def __init__(self, *args, **kwds):
        dict.__init__(self, *args, **kwds)
        self.__dict__ = self

    def load(self):
        table = load_csvfile(self, "research")
        for row in table:
            research_id = int(row["id"])
            step = int(row["step"])
            value = row["value"]
            lab_level = int(row["lab_level"])
            condition_id_1 = int(row["condition_id_1"])
            condition_step_1 = int(row["condition_step_1"])
            condition_id_2 = int(row["condition_id_2"])
            condition_step_2 = int(row["condition_step_2"])
            item1 = int(row["item1"])
            item2 = int(row["item2"])
            item3 = int(row["item3"])
            item4 = int(row["item4"])
            item5 = int(row["item5"])
            item1_qty = int(row["item1_qty"])
            item2_qty = int(row["item2_qty"])
            item3_qty = int(row["item3_qty"])
            item4_qty = int(row["item4_qty"])
            item5_qty = int(row["item5_qty"])
            research_sec = int(row["research_sec"])

            research_list.append(
                Research(
                    research_id = research_id,
                    step = step,
                    value = value,
                    lab_level = lab_level,
                    condition_id_1 = condition_id_1,
                    condition_step_1 = condition_step_1,
                    condition_id_2 = condition_id_2,
                    condition_step_2 = condition_step_2,
                    item1 = item1,
                    item2 = item2,
                    item3 = item3,
                    item4 = item4,
                    item5 = item5,
                    item1_qty = item1_qty,
                    item2_qty = item2_qty,
                    item3_qty = item3_qty,
                    item4_qty = item4_qty,
                    item5_qty = item5_qty,
                    research_sec = research_sec,
                    )
                )

    def get(self):
        return research_list

