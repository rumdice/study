#!/bin/bash

cd /home/owl/project/gameserver
source venv/bin/activate
cd scripts/arena

python arena_reward_normal.py 2>&1 tee -a arena_reward_normal.log
