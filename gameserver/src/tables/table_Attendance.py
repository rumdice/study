from src.common.util import load_csvfile

tier_attendance = {}
new_attendance = []
event_controller = {}

class Attendance(dict):
    def __init__(self, *args, **kwds):
        dict.__init__(self, *args, **kwds)
        self.__dict__ = self

    def _get_event_table(name):
        if "tier_attendance" == name:
            return tier_attendance
        if "new_attendance" == name:
            return new_attendance

    def load_tier(self):
        table = load_csvfile(self, "tier_attendance")
        for row in table:
            tier = int(row["tier"])
            reward = int(row["reward"])

            if not tier_attendance.get(tier, None):
                reward_list = []
                reward_list.append(0)
                reward_list.append(reward)
                tier_attendance[tier] = reward_list
            else:
                tier_attendance[tier].append(reward)

    def load_new(self):
        table = load_csvfile(self, "new_attendance")
        new_attendance.append(0)
        for row in table:
            reward = int(row["reward"])
            new_attendance.append(reward)

    def load_event(self):
        table = load_csvfile(self, "event_controller")
        for row in table:
            id = int(row["id"])
            table_name = row["table_name"]
            duration_minute = int(row["duration"])

        event_controller[id] = Attendance(
            eventTable = Attendance._get_event_table(table_name),
            keep_time = duration_minute
        )

    def get_tier(self):
        return tier_attendance

    def get_event_controller(self):
        return event_controller