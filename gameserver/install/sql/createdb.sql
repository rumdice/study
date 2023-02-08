CREATE USER 'puzzle'@'%' IDENTIFIED BY 'puzzle!!';
CREATE USER 'puzzle'@'localhost' IDENTIFIED BY 'puzzle!!';

CREATE SCHEMA `Account` DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ;
GRANT ALL ON Account.* TO puzzle;

CREATE SCHEMA game00 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ;
GRANT ALL ON game00.* TO puzzle;

CREATE SCHEMA game01 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ;
GRANT ALL ON game01.* TO puzzle;

CREATE SCHEMA game02 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ;
GRANT ALL ON game02.* TO puzzle;

CREATE SCHEMA game03 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ;
GRANT ALL ON game03.* TO puzzle;

CREATE SCHEMA game04 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ;
GRANT ALL ON game04.* TO puzzle;

CREATE SCHEMA game05 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ;
GRANT ALL ON game05.* TO puzzle;

CREATE SCHEMA game06 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ;
GRANT ALL ON game06.* TO puzzle;

CREATE SCHEMA game07 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ;
GRANT ALL ON game07.* TO puzzle;

CREATE SCHEMA game08 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ;
GRANT ALL ON game08.* TO puzzle;

CREATE SCHEMA game09 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ;
GRANT ALL ON game09.* TO puzzle;

CREATE SCHEMA guild DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ;
GRANT ALL ON guild.* TO puzzle;

CREATE SCHEMA guildinfo00 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ;
GRANT ALL ON guildinfo00.* TO puzzle;

CREATE SCHEMA guildinfo01 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ;
GRANT ALL ON guildinfo01.* TO puzzle;

CREATE SCHEMA guildinfo02 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ;
GRANT ALL ON guildinfo02.* TO puzzle;

CREATE SCHEMA guildinfo03 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ;
GRANT ALL ON guildinfo03.* TO puzzle;

CREATE SCHEMA guildinfo04 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ;
GRANT ALL ON guildinfo04.* TO puzzle;

CREATE SCHEMA guildinfo05 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ;
GRANT ALL ON guildinfo05.* TO puzzle;

CREATE SCHEMA guildinfo06 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ;
GRANT ALL ON guildinfo06.* TO puzzle;

CREATE SCHEMA guildinfo07 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ;
GRANT ALL ON guildinfo07.* TO puzzle;

CREATE SCHEMA guildinfo08 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ;
GRANT ALL ON guildinfo08.* TO puzzle;

CREATE SCHEMA guildinfo09 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ;
GRANT ALL ON guildinfo09.* TO puzzle;

CREATE SCHEMA LogDB00 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ;
GRANT ALL ON LogDB00.* TO puzzle;

CREATE SCHEMA LogDB01 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ;
GRANT ALL ON LogDB01.* TO puzzle;

CREATE SCHEMA LogDB02 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ;
GRANT ALL ON LogDB02.* TO puzzle;

CREATE SCHEMA LogDB03 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ;
GRANT ALL ON LogDB03.* TO puzzle;

CREATE SCHEMA LogDB04 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ;
GRANT ALL ON LogDB04.* TO puzzle;

CREATE SCHEMA LogDB05 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ;
GRANT ALL ON LogDB05.* TO puzzle;

CREATE SCHEMA LogDB06 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ;
GRANT ALL ON LogDB06.* TO puzzle;

CREATE SCHEMA LogDB07 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ;
GRANT ALL ON LogDB07.* TO puzzle;

CREATE SCHEMA LogDB08 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ;
GRANT ALL ON LogDB08.* TO puzzle;

CREATE SCHEMA LogDB09 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ;
GRANT ALL ON LogDB09.* TO puzzle;

CREATE SCHEMA adminTool DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ;
GRANT ALL ON adminTool.* TO puzzle;