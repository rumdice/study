DROP USER `root`@`%`;
CREATE USER 'root'@'%' IDENTIFIED BY 'PASSWORD';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;

DROP USER `puzzle`@`%`;
DROP USER `puzzle`@`localhost`;

CREATE USER `puzzle`@`%` IDENTIFIED BY 'puzzle!!';
CREATE USER `puzzle`@`localhost` IDENTIFIED BY 'puzzle!!';

CREATE SCHEMA `account` DEFAULT CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci;
CREATE SCHEMA `game` DEFAULT CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci;
CREATE SCHEMA `guild` DEFAULT CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci;
CREATE SCHEMA `guildinfo` DEFAULT CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci;
CREATE SCHEMA `logdb` DEFAULT CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci;
CREATE SCHEMA `admintool` DEFAULT CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci;

GRANT ALL ON account.* TO puzzle;
GRANT ALL ON game.* TO puzzle;
GRANT ALL ON guild.* TO puzzle;
GRANT ALL ON guildinfo.* TO puzzle;
GRANT ALL ON logdb.* TO puzzle;
GRANT ALL ON admintool.* TO puzzle;

FLUSH PRIVILEGES;
