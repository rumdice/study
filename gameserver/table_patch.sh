#!/bin/bash

cp /home/owl/project/gamedata/*.csv /home/owl/project/gameserver/gamedata

cd /home/owl/project/gameserver
source venv/bin/activate
cd conf

uwsgi --honour-stdin --harakiri=1200 --py-autoreload=2 --reload webapp.pid
# uwsgi --log-master --honour-stdin --harakiri=3600 --py-autoreload=2 --ini service_local.ini &

echo UWSGI Server Reloaded...
