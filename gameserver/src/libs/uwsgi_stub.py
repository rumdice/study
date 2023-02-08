# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

cache = {}
current_time = datetime.now()

opt = {
    "inifile": b"service_local.ini",
    "packet-log": "true",
    "performance-log": "true"
}


class cache_item(object):
    def __init__(self, value, expire_time):
        self.value = value
        self.expire_time = expire_time


def cache_get(key):
    if key in cache:
        if cache[key].expire_time > get_current_time():
            return cache[key].value
        else:
            cache_del(key)
    return None


def cache_set(key, value, expires=0):
    item = cache_item(value, datetime.max if expires == 0 \
        else get_current_time() + timedelta(seconds=expires))
    cache[key] = item


def cache_del(key):
    del cache[key]


def cache_update(key, value, expires=0):
    if key in cache:
        cache_set(key, value, expires)


def set_current_time(now):
    global current_time
    current_time = now


def get_current_time():
    return current_time
