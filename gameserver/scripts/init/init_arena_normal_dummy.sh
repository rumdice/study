#!/bin/bash

cd /home/owl/project/gameserver
source venv/bin/activate

python init_arena_normal_dummy.py 2>&1 tee -a init_arena_normal_dummy.log
