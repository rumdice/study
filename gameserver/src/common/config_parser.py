# -*- coding: utf-8 -*-
import os
from configparser import *


class GameServerConfigParser(ConfigParser):
    def __init__(self, **kwargs):
        self.basedir = kwargs.pop("basedir", None)
        ConfigParser.__init__(self)

    def _process_default_file(self):
        default = None
        try:
            default = self.get("default", "default")
            # 만일 basedir 이 설정된 상태이고, default경로가 절대 경로가 아니면, basedir 을 옮겨준다.
            if self.basedir is not None and not os.path.isabs(default):
                default = "{0}/{1}".format(self.basedir, default)

        except NoSectionError:
            pass
        except NoOptionError:
            pass
        except DuplicateOptionError:
            pass

        if default is not None:
            read_ok = ConfigParser.read(self, default)
            if len(read_ok) == 0 or read_ok[0] is None:
                raise Exception("default file not found : {0} ".format(default))

    def read(self, filenames):
        read_ok = ConfigParser.read(self, filenames)
        self._process_default_file()
        return read_ok
