# -*- coding: utf-8 -*-
from datetime import datetime

from src.common.logger import register_logger


@register_logger('session')
class Session(object):
    SESSION_EXPIRE_TIME = 10800
    SESSION_LENGTH = 18

    def __init__(self, factory):
        self.factory = factory
        self.redis_conn = self.factory.redis()

    @staticmethod
    def session_key(session_id):
        return "session:" + str(session_id)

    @staticmethod
    def userid_key(userid):
        return "userid:" + str(userid)

    def clear(self):
        self.redis_conn.flushdb()

    def set_sesion_id(self, session_id, packed_userid, nickname, serial):
        session_key = self.session_key(session_id)
        pipeline = self.redis_conn.pipeline()
        info_dict = {}
        info_dict['userid'] = packed_userid
        info_dict['nickname'] = nickname
        info_dict['serial'] = serial

        old_session = self.redis_conn.get(packed_userid)
        if old_session:
            self.redis_conn.delete(self.session_key(old_session))

        # pipeline.hmset(session_key, info_dict)
        pipeline.hset(session_key, mapping=info_dict)
        pipeline.expire(session_key, self.SESSION_EXPIRE_TIME)
        pipeline.setex(packed_userid, self.SESSION_EXPIRE_TIME, session_id)
        pipeline.execute()

    def generate_session_id(self, userid, nickname, serial):
        time_now = datetime.now()
        session_id = '9{0:02d}'.format(time_now.second)
        if 10 <= time_now.second:
            session_id = '{0:02d}'.format(time_now.second)
            
        session_id += '{0:010d}'.format(userid) + '{0:06d}'.format(time_now.microsecond)
        self.set_sesion_id(session_id, userid, nickname, serial)
        return int(session_id)

    def clear_session_id(self, session_id):
        self.redis_conn.delete(self.session_key(session_id))

    def get_session_info(self, session_id, write_redis, serial):
        session_info = self.redis_conn.hgetall(self.session_key(session_id))
        if session_info:
            check_serial = int(session_info["serial"]) + 1
            if check_serial != serial:
                return None
            write_redis.redis_conn.hset(self.session_key(session_id), "serial", str(check_serial))
            write_redis.redis_conn.expire(self.session_key(session_id), self.SESSION_EXPIRE_TIME)
            return (session_info['userid'], session_info['nickname'])
        return None