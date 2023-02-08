#!/bin/bash

cd /home/owl/project/gameserver/
source venv/bin/activate
cd scripts/arena

python arena_start_tournament.py 2>&1 tee -a arena_start_tournament.log
