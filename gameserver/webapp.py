# -*- coding: utf-8 -*-
import os
import sys
import traceback

from src.common.logmgr import *
from src.common.util import *
from src.context import *
from src.libs import uwsgi_stub as uwsgi
from src.service import WebAppService
from src.tables.table_Base import *

conf_dir = os.path.dirname(os.path.abspath(__file__)) + "/conf/"
logini = conf_dir + "logging_ws.ini"
LoggerManager.init("webapp")
logger = LoggerManager.getLogger()

sys.stdout = StringFilter(sys.stdout)
sys.stderr = JsonFilter(sys.stderr)

inifile = uwsgi.opt["inifile"]
inifile_utf8 = str(inifile, encoding="utf-8")
servive_ini = conf_dir + inifile_utf8

context = GameServerContext(
    inifile = servive_ini,
    table = TableBase,
    after_init = init_callback,
)

def application(env, start_response):
    try:
        request_size = int(env.get("CONTENT_LENGTH", 0))
    except ValueError:
        request_size = 0

    try:
        service = WebAppService(context)
        service.set_peer(env.get("REMOTE_ADDR", ""))
        service.set_user_agent(env.get("USER_AGENT", ""))

        request_body = env["wsgi.input"].read(request_size)
        response_body = service.process_raw_request(request_body)

        if response_body:
            start_response(
                "200 OK",
                [
                    ("Content-Type", "application/application/x-google-protobuf"),
                    ("Content-Length", str(len(response_body))),
                ],
            )
            return [response_body]
        else:
            logger.error("400 Bad Request")
            start_response("400 Bad Request", [("Content-Type", "application/x-google-protobuf")])
            return [""]
    except Exception as e:
        logger.error("Exception raise", exc_info=traceback)
        start_response("404 Error", [("Content-Type", "application/octet-stream")])
        return [""]

if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    app.wsgi_app = application
    app.run(host="0.0.0.0", port=8888)