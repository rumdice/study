#!/bin/bash
mysqldump --no-data -u root -p1111 -d --opt Account > account.sql
mysqldump --no-data -u puzzle -ppuzzle!! -d --opt game00 > game.sql
mysqldump --no-data -u puzzle -ppuzzle!! -d --opt guild  > guild.sql
mysqldump --no-data -u puzzle -ppuzzle!! -d --opt guildinfo00 > guildinfo.sql
mysqldump --no-data -u puzzle -ppuzzle!! -d --opt adminTool  > adminTool.sql
mysqldump --no-data -u puzzle -ppuzzle!! -d --opt LogDB00 > LogDB.sql
