# -*- encoding: utf-8 -*-
import json
import logging
import sys

import sqlalchemy

log = logging.getLogger(__name__)


class Mapper(object):
    def __init__(self, metadata):
        self.metadata = metadata
        self.tables = self.metadata.tables


class SqlSession(object):
    def __init__(self, factory):
        self.factory = factory
        self.engine = factory.engine
        self.metadata = factory.metadata
        self.connection = self.engine.connect()
        self.trans = None

    def _call_func(self, mapper, *args, **kwargs):
        func = self.factory.get_mapper_func(mapper, self)
        return func(*args, **kwargs)

    def _execute(self, mapper, *args, **kwargs):
        query = self._call_func(mapper, *args, **kwargs)
        if query is None:
            raise Exception("query is not define")
        return self.connection.execute(query)

    def call_procedure(self, function_name, params):
        connections = self.engine.raw_connection()
        try:
            cursor = connections.cursor()
            cursor.callproc(function_name, params)
            results = list(cursor.fetchall())
            cursor.close()
            connections.commit()
            return results
        finally:
            connections.close()
            return

    def update_column_userid(self, table, update_value, key):
        query = ("UPDATE %s SET %s WHERE auid = %s") % (table, update_value, key)
        self.connection.execute(query)
        return
    
    def update_column_doublekey(self, table, key, data):
        query = ("UPDATE %s SET %s WHERE %s") % (table, data, key)
        self.connection.execute(query)
        return

    def select_profile_column(self, table, columns, key):
        query = ("SELECT %s FROM %s WHERE auid = %s") % (columns, table, key)
        row = self.connection.execute(query).fetchone()
        return row

    def add_item_count(self, user_id, item_id, add_count):
        query = ("INSERT INTO tb_inven_etc (auid, item_id, item_count) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE item_count=item_count+%s") % (user_id, item_id, add_count, add_count)
        self.connection.execute(query)
        return

    def add_research_step(self, user_id, research_id, add_step):
        query = ("INSERT INTO tb_research (auid, research_id, step) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE step=step+%s") % (user_id, research_id, add_step, add_step)
        self.connection.execute(query)
        return

    def add_guild_member(self, guild_uid, member_uid, grade):
        query = ("INSERT INTO tb_guild_member( guild_uid, auid, guild_grade, raid_record) VALUES (%s, %s, %s, '[]') ON DUPLICATE KEY UPDATE guild_uid=%s, guild_grade=%s") % ( guild_uid, member_uid, grade, guild_uid, grade)
        self.connection.execute(query)
        return

    def add_guild_raid_damage(self, guild_uid, member_uid, damage):
        query = ("INSERT INTO tb_guild_raid_damage (guild_uid, auid, total_damage) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE total_damage=total_damage+%s") % (guild_uid, member_uid, damage, damage)
        self.connection.execute(query)
        return

    def add_guild_contest_damage(self, guild_uid, member_uid, damage):
        query = ("INSERT INTO tb_guild_contest_damage (guild_uid, auid, total_damage) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE total_damage=total_damage+%s") % (guild_uid, member_uid, damage, damage)
        self.connection.execute(query)
        return

    def update_guild_contest_record(self, guild_uid, member_uid, damage):
        query = ("INSERT INTO tb_guild_contest_damage (guild_uid, auid, total_damage) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE total_damage=total_damage+%s") % (guild_uid, member_uid, damage, damage)
        self.connection.execute(query)
        return
    
    def insert_update_territory_build(self, user_id, build_uid, level, type, time):
        query = ("INSERT INTO tb_territory_build (uid, auid, building_type, build_level, create_time) VALUES (%s, %s, %s, %s, '%s') ON DUPLICATE KEY UPDATE build_level=%s") % (build_uid, user_id, type, level, time, level)
        self.connection.execute(query)
        return



    def begin(self):
        self.trans = self.connection.begin()

    def commit(self):
        if self.trans is not None and self.trans.is_active:
            self.trans.commit()

    def close(self):
        if self.connection is not None:
            self.connection.close()

    def rollback(self):
        if self.trans is not None and self.trans.is_active:
            self.trans.rollback()

    def update(self, mapper, *args, **kwargs):
        return self._execute(mapper, *args, **kwargs)

    def query_for_value(self, mapper, *args, **kwargs):
        try:
            val = self._execute(mapper, *args, **kwargs).scalar() or 0
            return val
        except Exception as e:
            print(e, file=sys.stderr)
            return 0

    def query_one_or_none(self, mapper, *args, **kwargs):
        row = self._execute(mapper, *args, **kwargs).one()
        return row

    def query_for_one(self, mapper, *args, **kwargs):
        row = self._execute(mapper, *args, **kwargs).fetchone()
        return row

    def query_for_sum(self, mapper, *args, **kwargs):
        row = self._execute(mapper, *args, **kwargs).fetchall(); result = sum(value[0] if value[0] is not None else 0 for value in row)
        return result

    def query_for_all(self, mapper, *args, **kwargs):
        rows = self._execute(mapper, *args, **kwargs).fetchall()
        return rows

    def delete(self, mapper, *args, **kwargs):
        return self._execute(mapper, *args, **kwargs)

    def insert(self, mapper, *args, **kwargs):
        return self._execute(mapper, *args, **kwargs)

    def __enter__(self):
        if self.connection is not None:
            self.begin()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection is not None:
            if exc_type:
                self.rollback()
            else:
                self.commit()

    def __del__(self):
        self.close()


class SqlSessionConfigure(object):
    DEFAULT_POOLSIZE = 4

    def __init__(self, connstring, **kwargs):
        options = kwargs.pop("options", {})

        options.update(kwargs)
        options.update({
            'pool_timeout': options.pop('pool_timeout', 30),
            'pool_recycle': options.pop('pool_recycle', 500),
            'pool_size': options.pop('pool_size', SqlSessionConfigure.DEFAULT_POOLSIZE),
            'pool_reset_on_return': options.pop('pool_reset_on_return', None),
        })

        self.conn_params = options
        self.conn_string = connstring
        self.mappers = {}
        self.mapping_callback = None

    def add_mapper(self, *mappers):
        for mapper in mappers:
            if not issubclass(mapper, Mapper):
                raise TypeError("{0} is not Mapper subclass".format(mapper))

            mapper_name = mapper.__name__

            if self.mappers.get(mapper_name):
                raise Exception("{0} already registered".format(mapper))

            self.mappers[mapper_name] = mapper


class SqlSessionConfigureWithConfig(SqlSessionConfigure):
    def __init__(self, configuration, prefix=None, **kwargs):
        options = dict((key[len(prefix):], value)
                       for key, value in configuration
                       if key.startswith(prefix))

        options.update(kwargs)
        options['_coerce_config'] = True
        conn_string = options.pop('_url')
        SqlSessionConfigure.__init__(self, conn_string, options=options, **kwargs)


class SqlSessionMap(object):
    def __init__(self):
        self.sqlsession_map = {}

    def add(self, key, sqlsession):
        self.sqlsession_map[key] = sqlsession

    def get_session(self, userid):
        return self.sqlsession_map[userid % Sql4PartitionedSessionFactory.key_len]

    def begin(self):
        for k, v in self.sqlsession_map.items():
            _k = k
            v.begin()

    def commit(self):
        for k, v in self.sqlsession_map.items():
            _k = k
            v.commit()

    def rollback(self):
        for k, v in self.sqlsession_map.items():
            _k = k
            v.rollback()


class Sql4PartitionedSessionFactory(object):
    def __init__(self, session_configure, key_len):
        self.factories = {}
        self.key_len = None

        json_connstring = session_configure.conn_string
        connstring_dict = json.loads(json_connstring)

        self.key_len = key_len

        for conn_string in connstring_dict:
            key = conn_string["key"]
            url = conn_string["url"]

            if self.factories.get(key) is not None:
                raise KeyError("Already Asigned Connection : key:{}, url:{}", key, url)

            session_configure.conn_string = url
            self.factories[int(key)] = SqlSessionFactory(session_configure)

        if len(self.factories) != self.key_len:
            raise Exception("Key Error: need {} keys", self.key_len)

    def _get_factory(self, userid):
        return self.factories[userid % self.key_len]

    def session(self, userid):
        return SqlSession(self._get_factory(userid))

    def session_map(self):
        session_map = SqlSessionMap()
        for k in range(0, self.key_len):
            session_map.add(k, self.session(k))
        return session_map

    def session_all(self):
        for k, v in self.factories.items():
            yield SqlSession(v)

class SqlSessionFactory(object):
    def __init__(self, session_configure):
        conn_string = session_configure.conn_string
        conn_param = session_configure.conn_params
        mappers = session_configure.mappers
        self.metadata = None
        self.mappers = None
        self.database_name = None
        self.engine = sqlalchemy.create_engine(conn_string, **conn_param)
        self.database_name = self.engine.url.database
        self._init_metadata(self.engine, session_configure.mapping_callback)
        self._register_mapper(mappers)

    def _register_mapper(self, mappers):
        self.mappers = mappers

    def _init_metadata(self, engine, callback):
        self.metadata = sqlalchemy.MetaData(schema=self.database_name)
        self.metadata.reflect(engine)

        if callback is not None:
            callback(self.metadata)

    def get_mapper_func(self, mapper_name, session):
        clz_name, func_name = mapper_name.rsplit('.', 1)
        clz = self.mappers.get(clz_name)
        if clz is None:
            raise LookupError("%s mapper not found" % (clz_name))
        return getattr(clz(session.metadata), func_name)

    def session(self, userid=None):
        return SqlSession(self)
