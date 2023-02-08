#!/bin/bash
. rp_venv/bin/activate
cd gameserver/conf/
uwsgi --stop /home/owl/owlserver/gameserver/conf/webapp.pid 
# uwsgi --stop wepapp.pid
# sudo killall -9 uwsgi
