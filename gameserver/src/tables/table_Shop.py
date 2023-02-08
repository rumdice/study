from src.common.util import load_csvfile

return_point = {}
arena_coin = {}


class Shop(dict):
    def __init__(self, *args, **kwds):
        dict.__init__(self, *args, **kwds)
        self.__dict__ = self

    def load_return_point(self):
        table = load_csvfile(self, "returnPointShop")
        for row in table:
            shop_id = int(row["id"])
            price = int(row["price"])
            reward = int(row["reward"])

            buy_limit_type = int(row["buy_limit_type"])
            limit_qty = int(row["limit_qty"])
            return_point[shop_id] = Shop(
                shop_id = shop_id,
                price = price,
                reward = reward,
                reward_item_count = 0,
                buy_limit_type = buy_limit_type,
                limit_qty = limit_qty
            )


    def load_arena_coin(self):
        table = load_csvfile(self, "arenaCoinShop")
        for row in table:
            shop_id = int(row["id"])
            price = int(row["price"])
            reward = int(row["reward"])

            buy_limit_type = int(row["buy_limit_type"])
            limit_qty = int(row["limit_qty"])
            arena_coin[shop_id] = Shop(
                shop_id = shop_id,
                price = price,
                reward = reward,
                reward_item_count = 0,
                buy_limit_type = buy_limit_type,
                limit_qty = limit_qty
            )


    def get_return_point(self):
        return return_point

    def get_arena_coin(self):
        return arena_coin