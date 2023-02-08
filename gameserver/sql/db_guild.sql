/*
SQLyog Community v13.1.9 (64 bit)
MySQL - 10.5.8-MariaDB-1:10.5.8+maria~focal : Database - db_guild
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`db_guild` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci */;

USE `db_guild`;

/*Table structure for table `tb_guild` */

DROP TABLE IF EXISTS `tb_guild`;

CREATE TABLE `tb_guild` (
  `guild_uid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `guild_name` varchar(255) NOT NULL,
  `guild_master` int(10) unsigned DEFAULT NULL,
  `guild_bg` int(10) unsigned DEFAULT NULL,
  `guild_emblem` int(10) unsigned DEFAULT NULL,
  `guild_create` datetime DEFAULT NULL,
  PRIMARY KEY (`guild_uid`),
  UNIQUE KEY `nick_idx` (`guild_name`)
) ENGINE=MyISAM AUTO_INCREMENT=305 DEFAULT CHARSET=utf8;

/*Table structure for table `tb_guild_contest_damage` */

DROP TABLE IF EXISTS `tb_guild_contest_damage`;

CREATE TABLE `tb_guild_contest_damage` (
  `guild_uid` int(11) NOT NULL,
  `auid` int(11) NOT NULL,
  `total_damage` int(11) NOT NULL,
  PRIMARY KEY (`auid`,`guild_uid`),
  KEY `guild_idx` (`guild_uid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

/*Table structure for table `tb_guild_member` */

DROP TABLE IF EXISTS `tb_guild_member`;

CREATE TABLE `tb_guild_member` (
  `guild_uid` int(10) unsigned NOT NULL,
  `auid` int(10) unsigned NOT NULL,
  `guild_grade` int(10) unsigned DEFAULT NULL,
  `raid_start_time` datetime DEFAULT NULL,
  `raid_record` longtext DEFAULT NULL,
  `reward_grade` int(11) DEFAULT 0,
  `reward_damage` int(11) DEFAULT 0,
  `reward_flag` tinyint(4) DEFAULT 0,
  `contest_start_time` datetime DEFAULT NULL,
  `contest_damage_record` longtext DEFAULT NULL,
  `contest_reward_time` datetime DEFAULT NULL,
  `grade_promote_time` datetime DEFAULT NULL,
  PRIMARY KEY (`auid`),
  KEY `uid` (`guild_uid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

/*Table structure for table `tb_guild_raid_damage` */

DROP TABLE IF EXISTS `tb_guild_raid_damage`;

CREATE TABLE `tb_guild_raid_damage` (
  `guild_uid` int(11) NOT NULL,
  `auid` int(11) NOT NULL,
  `total_damage` int(11) NOT NULL,
  PRIMARY KEY (`auid`,`guild_uid`),
  KEY `guild_idx` (`guild_uid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

/*Table structure for table `tb_guildinfo` */

DROP TABLE IF EXISTS `tb_guildinfo`;

CREATE TABLE `tb_guildinfo` (
  `guild_uid` int(11) NOT NULL,
  `guild_point` int(11) NOT NULL DEFAULT 0,
  `member_count` int(11) NOT NULL DEFAULT 1,
  `join_level` int(11) DEFAULT NULL,
  `join_type` int(11) DEFAULT NULL,
  `guild_msg` varchar(255) DEFAULT NULL,
  `raid_monster` int(11) DEFAULT 0,
  `raid_element` int(11) DEFAULT 0,
  `raid_monster_hp` int(11) DEFAULT 0,
  `raid_monster_level` int(11) DEFAULT 1,
  `raid_complete_count` int(11) DEFAULT 0,
  `contest_enemy_guild_guid` int(11) DEFAULT NULL,
  `contest_monster` int(11) DEFAULT 0,
  `contest_element` int(11) DEFAULT 0,
  `contest_monster_hp` int(11) DEFAULT 0,
  `contest_monster_level` int(11) DEFAULT 0,
  `contest_complete_count` int(11) DEFAULT 0,
  PRIMARY KEY (`guild_uid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

/*Table structure for table `tb_raid_result` */

DROP TABLE IF EXISTS `tb_raid_result`;

CREATE TABLE `tb_raid_result` (
  `guild_uid` int(11) NOT NULL,
  `raid_monster` int(11) DEFAULT 0,
  `element` int(11) DEFAULT 0,
  `monster_hp` int(11) DEFAULT 0,
  `monster_level` int(11) DEFAULT 0,
  `damage_record` longtext DEFAULT NULL,
  PRIMARY KEY (`guild_uid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
