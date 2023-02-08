#!/bin/bash

cd /home/owl/project/gameserver
source venv/bin/activate

python init_cache.py 2>&1 tee -a init_cache.log
