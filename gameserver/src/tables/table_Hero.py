from src.common.util import load_csvfile
from src.protocol.webapp_pb import Define

hero = {}
start = []
return_point = []
passive_skill = []

class Hero():
    def __init__(self, id, hp, jclass, element, grade, group):
        self.index = id
        self.hp = hp
        self.jclass = jclass
        self.element = element
        self.item_type = Define.ITEM_TYPE_HERO
        self.grade = grade
        self.promotion_group = group

    def load(self):
        table = load_csvfile(self, "hero")
        for row in table:
            index = int(row["id"])
            hp = int(row["HP"])
            jclass = int(row["jclass"])
            element = int(row["element"])
            grade = int(row["grade"])
            promotion_group = int(row["promotion"])
            hero[index] = Hero(index, hp, jclass, element, grade, promotion_group)

    def get(self):
        return hero

class HeroBunch(dict):
    def __init__(self, *args, **kwds):
        dict.__init__(self, *args, **kwds)
        self.__dict__ = self

    def load_start(self):
        table = load_csvfile(self, "start_hero")
        for row in table:
            type = int(row["type"])
            value = int(row["value"])
            count = int(row["position"])
            start.append(
                HeroBunch(
                    type = type,
                    value = value,
                    count = count
                )
            )


    def load_return(self):
        return_point.append(0)
        table = load_csvfile(self, "hero_return")
        for row in table:
            point = int(row["point"])
            return_point.append(point)
        

    def load_passive_skill(self):
        table = load_csvfile(self, "passive_skill")
        for row in table:
            _jclass = int(row["class"])
            _grade1 = int(row["grade1"])
            _grade2 = int(row["grade2"])
            _grade3 = int(row["grade3"])
            passive_skill.append(
                HeroBunch(
                    jclass = _jclass, 
                    grade1 = _grade1,
                    grade2 = _grade2,
                    grade3 = _grade3
                )
            )


    def get_start(self):
        return start

    def get_return_point(self):
        return return_point

    def get_passive_skill(self):
        return passive_skill

    