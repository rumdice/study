#!/bin/bash

cd /home/owl/project/gameserver
source venv/bin/activate
cd scripts/arena

python arena_recovery_normal.py 2>&1 tee -a arena_recovery_normal.log
