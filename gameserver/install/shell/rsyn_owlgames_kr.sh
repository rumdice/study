#!/bin/bash

cd /home/owl/project/gameserver
tar cvf src.tar src
scp -i ~/.ssh/owlgames-kr  src.tar ubuntu@13.125.198.12:~
