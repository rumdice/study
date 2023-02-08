#!/bin/bash
mysqldump --no-data -u root -p1111 -d --opt Account -d --single-transaction | sed 's/ AUTO_INCREMENT=[0-9]*\b//' > account.sql
mysqldump --no-data -u puzzle -ppuzzle!! -d --opt game0 -d --single-transaction | sed 's/ AUTO_INCREMENT=[0-9]*\b//' > game.sql
mysqldump --no-data -u puzzle -ppuzzle!! -d --opt guild -d --single-transaction | sed 's/ AUTO_INCREMENT=[0-9]*\b//' > guild.sql
mysqldump --no-data -u puzzle -ppuzzle!! -d --opt guildinfo0 -d --single-transaction | sed 's/ AUTO_INCREMENT=[0-9]*\b//' > guildinfo.sql
mysqldump --no-data -u puzzle -ppuzzle!! -d --opt adminTool -d --single-transaction | sed 's/ AUTO_INCREMENT=[0-9]*\b//' > adminTool.sql
mysqldump --no-data -u puzzle -ppuzzle!! -d --opt LogDB -d --single-transaction | sed 's/ AUTO_INCREMENT=[0-9]*\b//' > LogDB.sql
