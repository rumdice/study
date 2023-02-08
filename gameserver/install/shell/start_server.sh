#!/bin/bash
. rp_venv/bin/activate
cd gameserver/conf/
uwsgi service_local.ini