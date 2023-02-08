# -*- coding: utf-8 -*-
import sys
from configparser import NoSectionError

import redis
from src.common.logger import register_logger


class RedisConfig(object):
    DEFAULT_POOL_SIZE = 5

    def __init__(self, configuration, prefix):
        options = dict((key[len(prefix):], value) for key, value in configuration if key.startswith(prefix))

        if 'db' not in options:
            raise NoSectionError('redis-db option is not found.')

        host = options.pop('host', 'localhost')
        if host.startswith('['):
            host = host[1:len(host) - 1].replace(' ', '').strip(',')

        options.update({
            'password' : options.pop('pwd', ''),
            'host': host,
            'port': options.pop('port', 6379),
            'db': options.pop('db', None)
        })

        self.max_connections = int(options.pop('max_connections', RedisConfig.DEFAULT_POOL_SIZE))
        self.conn_param = options


class RedisPoolSelector(object):
    SINGLE_POOL = 0
    MULTI_POOL = 1

    def __init__(self, pools, mode=SINGLE_POOL):
        self.pools = pools
        self.mode = mode

    def select(self, userid):
        if self.mode == RedisPoolSelector.MULTI_POOL:
            return self.choose_pool(userid)
        else:
            return self.pools[0]

    def choose_pool(self, userid):
        _userid = userid
        return self.pools[0]


@register_logger('redis.factory')
class RedisConnectionFactory(object):
    class RedisPool(object):
        def __init__(self, max_connections, conn_param):
            self.host = conn_param.get('host')
            self.port = conn_param.get('port')
            self.db = conn_param.get('db')

            try:
                self.redis = redis.StrictRedis(
                    connection_pool= redis.ConnectionPool(
                        max_connections = max_connections,
                        decode_responses = True,
                        **conn_param
                    )
                )
            except Exception as e:
                print(e, file=sys.stderr)

    def __init__(self, configure):
        self.pools = []
        self.pool_selector = None
        hosts = configure.conn_param['host']
        if type(hosts) is list:
            for host in hosts:
                conn_param = configure.conn_param
                conn_param.update({'host': host})
                self.pools.append(RedisConnectionFactory.RedisPool(
                    max_connections = configure.max_connections,
                    conn_param = conn_param
                    )
                )
                self.pool_selector = RedisPoolSelector(
                    self.pools, RedisPoolSelector.MULTI_POOL
                )
        else:
            self.pools.append(RedisConnectionFactory.RedisPool(
                max_connections = configure.max_connections,
                conn_param = configure.conn_param
                )
            )
            self.pool_selector = RedisPoolSelector(self.pools)

    def redis(self, userid=None):
        pool = self.pool_selector.select(userid)
        return pool.redis
