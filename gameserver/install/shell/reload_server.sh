#!/bin/bash
. rp_venv/bin/activate
cd gameserver/conf/
uwsgi --reload webapp.pid
# uwsgi --honour-stdin --harakiri=1200 --py-autoreload=2 --reload webapp.pid
