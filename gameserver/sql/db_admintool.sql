/*
SQLyog Community v13.1.9 (64 bit)
MySQL - 10.5.8-MariaDB-1:10.5.8+maria~focal : Database - db_admintool
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`db_admintool` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci */;

USE `db_admintool`;

/*Table structure for table `arena_tournament_info` */

DROP TABLE IF EXISTS `arena_tournament_info`;

CREATE TABLE `arena_tournament_info` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `group` int(11) NOT NULL,
  `day` int(11) NOT NULL,
  `total_count` int(11) NOT NULL,
  `start_time` datetime DEFAULT NULL,
  `round_day` int(11) NOT NULL DEFAULT 0,
  `user_count` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*Table structure for table `event_dungeon` */

DROP TABLE IF EXISTS `event_dungeon`;

CREATE TABLE `event_dungeon` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `dungeon_type` int(11) NOT NULL,
  `dungeon_id` int(11) NOT NULL,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  PRIMARY KEY (`uid`),
  UNIQUE KEY `event_dungeon_dungeon_type_IDX` (`dungeon_type`,`dungeon_id`) USING BTREE
) ENGINE=MyISAM AUTO_INCREMENT=129 DEFAULT CHARSET=utf8;

/*Table structure for table `guild_contest_info` */

DROP TABLE IF EXISTS `guild_contest_info`;

CREATE TABLE `guild_contest_info` (
  `uid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `start_time` datetime NOT NULL DEFAULT current_timestamp(),
  `end_time` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
