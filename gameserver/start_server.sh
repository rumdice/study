#!/bin/bash

cd /home/owl/project/gameserver
source venv/bin/activate
cd conf
uwsgi --log-master --honour-stdin --harakiri=3600 --py-autoreload=2 --ini service_local.ini &

echo UWSGI Server Started...
