# -*- coding: utf-8 -*-
import logging
import logging.config
import sys


class WebAppLogger(logging.Logger):
    pass


class LoggerManager(object):
    _root_logger = logging.getLogger()
    _childs = dict()

    def __init__(self):
        pass

    @classmethod
    def init(cls, name):
        logging.setLoggerClass(WebAppLogger)
        cls._root_logger = logging.getLogger(name)

    @classmethod
    def setLevel(cls, level):
        cls._root_logger.setLevel(level)

    @classmethod
    def getLogger(cls, name=None):
        if name is None:
            return cls._root_logger

        logger_name = "%s.%s" % (cls._root_logger.name, name)
        if logger_name in cls._childs:
            return cls._childs[logger_name]

        cls._childs[logger_name] = logging.getLogger(logger_name)
        return cls._childs[logger_name]

    @classmethod
    def addHandler(cls, handler):
        cls._root_logger.addHandler(handler)

    @classmethod
    def removeHandler(cls, handler):
        cls._root_logger.removeHandler(handler)


def register_logger(name=None):
    def decorator(clazz):
        clazz.logger = LoggerManager.getLogger(name)
        return clazz

    return decorator


def add_default_handler(logger):
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        "%(levelname)-9s %(asctime)s [%(module)s/%(funcName)s:%(lineno)d] %(message)s"))
    logger.addHandler(handler)
