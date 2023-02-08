from src.common.util import load_csvfile

goods = []
sell = []
buy = []


class MerchantGoods(object):
    def __init__(self, table_id, prob, goods_dict):
        self.table_id = table_id
        self.prob = prob
        self.goods_dict = goods_dict


class Trade(dict):
    def __init__(self, *args, **kwds):
        dict.__init__(self, *args, **kwds)
        self.__dict__ = self

    def load(self):
        goods.append(None)
        table = load_csvfile(self, "trade")
        for row in table:
            table_id = int(row["id"])
            probablity = int(row["probablity"])
            goods_dict = {}
            for i in range(8):
                csvcolumn = "item" + str(i+1)
                item_id = int(row[csvcolumn])
                if 0 >= item_id:
                    break

                csvcolumn = "product_qty" + str(i+1)
                sell_count = int(row[csvcolumn])

                csvcolumn = "buy_qty" + str(i+1)
                buy_count = int(row[csvcolumn])

                goods_dict[item_id] = Trade(
                    sell_count = sell_count,
                    buy_count = buy_count
                )

            goods.append(MerchantGoods(table_id, probablity, goods_dict))


    def load_item(self):
        table = load_csvfile(self, "trade_item")
        for row in table:
            type = int(row["type"])

            for i in range(8):
                strcolumn = "item" + str(i+1)
                item = int(row[strcolumn])
                if 0 >= item:
                    break

                strcolumn = "prob" + str(i+1)
                prob = int(row[strcolumn])

                if type == 1:
                    sell.append(
                        Trade(
                            item_id = item,
                            prob = prob
                        )
                    )
                else:
                    buy.append(
                        Trade(
                            item_id = item,
                            prob = prob
                        )
                    )

    def get(self):
        return goods
    
    def get_item_sell(self):
        return sell
    
    def get_item_buy(self):
        return buy

