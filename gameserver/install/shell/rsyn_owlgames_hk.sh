#!/bin/bash

cd /home/owl/project/gameserver
tar cvf src.tar src
scp -i ~/.ssh/owlgames-hk  src.tar ubuntu@18.166.228.177:~
