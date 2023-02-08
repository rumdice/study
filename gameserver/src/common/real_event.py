# -*- coding: utf-8 -*-
# import time

# from src.metalredis.redis_connection import RedisConfig, RedisConnectionFactory

# __author__ = 'tteogi'

# from src.noblesse_pb2 import Response

# UPDATE_DURATION = 60 * 10

# class RealEventData(object):
#     class DataFactory(object):

#         @staticmethod
#         def decode_reward(redis_dic, real_time_event_protocol):
#             real_time_event_protocol.reward_event.ParseFromString(redis_dic.get('data'))
#             return real_time_event_protocol.reward_event

#         @staticmethod
#         def decode_market_sale(redis_dic, real_time_event_protocol):
#             real_time_event_protocol.sale_event.ParseFromString(redis_dic.get('data'))
#             return real_time_event_protocol.sale_event

#         @staticmethod
#         def decode_monthly(redis_dic, real_time_event_protocol):
#             real_time_event_protocol.monthly_purchase_event.ParseFromString(redis_dic.get('data'))
#             return real_time_event_protocol.monthly_purchase_event

#         @staticmethod
#         def decode_purchase(redis_dic, real_time_event_protocol):
#             real_time_event_protocol.purchase_event.ParseFromString(redis_dic.get('data'))
#             return real_time_event_protocol.purchase_event

#         @staticmethod
#         def decode_buy_gold(redis_dic, real_time_event_protocol):
#             real_time_event_protocol.buy_gold_event.ParseFromString(redis_dic.get('data'))
#             return real_time_event_protocol.buy_gold_event

#         @staticmethod
#         def decode_mod_open(redis_dic, real_time_event_protocol):
#             real_time_event_protocol.mode_open_event.ParseFromString(redis_dic.get('data'))
#             return real_time_event_protocol.mode_open_event

#     # __event_factory = {
#     #     RealTimeEvent.MARKET_SALE: DataFactory.decode_market_sale,
#     #     RealTimeEvent.REWARD: DataFactory.decode_reward,
#     #     RealTimeEvent.MONTHLY_PURCHASE: DataFactory.decode_monthly,
#     #     RealTimeEvent.PURCHASE: DataFactory.decode_purchase,
#     #     RealTimeEvent.BUY_GOLD: DataFactory.decode_buy_gold,
#     #     RealTimeEvent.MODE_OPEN: DataFactory.decode_mod_open,
#     # }

#     def __init__(self, redis_dic, real_time_event_protocol):
#         self.__decode_default(redis_dic, real_time_event_protocol)

#     def __decode_default(self, redis_dic, real_time_event_protocol):
#         self.is_running = False
#         self.uid = int(redis_dic.get('event_uid'))
#         self.event_type = int(redis_dic.get('event_type'))
#         expire_date = redis_dic.get('expire_date')
#         start_date = redis_dic.get('start_date')
#         cur_time = time.time()
#         if start_date:
#             self.start_date = int(float(start_date))
#             if self.start_date > cur_time:
#                 return

#         if expire_date is not None:
#             self.expire_date = int(float(expire_date))
#             if cur_time < self.expire_date:
#                 self.is_running = True
#                 self.data = RealEventData.__event_factory[self.event_type](redis_dic, real_time_event_protocol)
#                 self.data.running.remain_second = self.expire_date - int(cur_time)

# # class RealEvent(object):
# #     def __init__(self, parser, prefix):
# #         config = parser.items('event_manager')
# #         configure = RedisConfig(config, 'redis-')
# #         self.__event_redis = RedisConnectionFactory(configure)
# #         self.__update_time = -1
# #         self.__running_events = {}
# #         self.__real_time_event_protocol = RealTimeEvent()
# #
# #     def get_redis_data(self, market_type):
# #         redis = self.__event_redis.redis()
# #         events = redis.hgetall(market_type)
# #         return events['data']
# #
# #     def get_running_events(self):
# #         cur_time = time.time()
# #         if self.__update_time < cur_time:
# #             self.__running_events.clear()
# #             self.__update_time = cur_time + UPDATE_DURATION
# #             redis = self.__event_redis.redis()
# #             event_types = RealTimeEvent.EventType.DESCRIPTOR.values
# #             pipeline = redis.pipeline()
# #             for running_event_type in event_types:
# #                 pipeline.hgetall(running_event_type.name)
# #             events = pipeline.execute()
# #             for event in events:
# #                 id = event.get('event_type')
# #                 if id is not None:
# #                     event_data = RealEventData(event, self.__real_time_event_protocol)
# #                     if event_data.is_running:
# #                         if self.__running_events.get(event_data.event_type):
# #                             raise Exception('same id real_time_event id: {} uid: {}'.format(
# #                                 event_data.uid, event_data.event_type))
# #                         self.__running_events[event_data.event_type] = event_data
# #         return self.__running_events
# #
# #     def get_response_running_events(self, response):
# #         self.get_running_events()
# #         response.real_time_event.CopyFrom(self.__real_time_event_protocol)
# #
# #     def set_event(self, event_type, mapping):
# #         redis = self.__event_redis.redis()
# #         redis.hmset(event_type, mapping)
# #
# #     def get_event_data(self, event_type):
# #         running_events = self.get_running_events()
# #         data = running_events.get(event_type)
# #         if data != None:
# #             if time.time() > data.expire_date:
# #                 running_events.pop(event_type, None)
# #                 return None
# #             else:
# #                 return data
# #
# #     def is_mode_event(self, stage_type):
# #         event = self.get_event_data(RealTimeEvent.MODE_OPEN)
# #         if event:
# #             for type in event.data.stage_types:
# #                 if type == stage_type:
# #                     return True
# #         return False
# #
# #     def get_reward_event_assets(self, stage_type):
# #         event = self.get_event_data(RealTimeEvent.REWARD)
# #         if event:
# #             for reward_stage in event.data.reward_stages:
# #                 if reward_stage.stage_type == stage_type:
# #                     return True
# #         return False
# #
# #     def get_sale_price(self, market_type, asset_type, price):
# #         event = self.get_event_data(RealTimeEvent.MARKET_SALE)
# #         if event:
# #             for market in event.data.markets:
# #                 if market.market_type == market_type:
# #                     sale = (1.0 - float(market.sale_percent) / 100.0)
# #                     return int(price * sale)
# #                     break
# #         return price
# #
# #     def get_monthly_purchase(self):
# #         return self.get_event_data(RealTimeEvent.MONTHLY_PURCHASE)
# #
# #     def get_purchase(self):
# #         return self.get_event_data(RealTimeEvent.PURCHASE)
# #
# #     def get_bonus_gold(self):
# #         return self.get_event_data(RealTimeEvent.BUY_GOLD)
# #
# #     def get_anniversary(self):
# #         return self.get_event_data(RealTimeEvent.ANNIVERSARY)
# #
# #     def flush(self):
# #         self.__update_time = -1
# #         self.__running_events = {}
# #         self.__event_redis.redis().flushdb()

#     # def __init__(self, *event_indexes, **kwargs):
#     #     self.__event_indexes = event_indexes
#     #
#     # def __call__(self, func):
#     #     def event_wrapper(service, request, response):
#     #         func(service, request, response)
#     #         if response.result != Response.SUCCESS:
#     #             return
#     #
#     #         self.set_event_response(request, response)
#     #     return event_wrapper
#     #
#     # def set_event_response(self, request, response):
#     #     for event_type in self.__event_indexes:
#     #         event = self.get_event_data(event_type)
#     #         if event is None:
#     #             continue

