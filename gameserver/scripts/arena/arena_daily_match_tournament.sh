#!/bin/bash

cd /home/owl/project/gameserver
source venv/bin/activate
cd scripts/arena

python arena_daily_match_tournament.py 2>&1 tee -a arena_daily_match_tournament.log
