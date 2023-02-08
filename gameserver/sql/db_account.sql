/*
SQLyog Community v13.1.9 (64 bit)
MySQL - 10.5.8-MariaDB-1:10.5.8+maria~focal : Database - db_account
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`db_account` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci */;

USE `db_account`;

/*Table structure for table `tb_account` */

DROP TABLE IF EXISTS `tb_account`;

CREATE TABLE `tb_account` (
  `account_uid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `web_userid` varchar(255) NOT NULL,
  `nick_name` varchar(255) NOT NULL,
  `account_type` int(10) unsigned NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `login_device` varchar(255) NOT NULL,
  `create_time` datetime DEFAULT NULL,
  `email` varchar(255) NOT NULL,
  `push_alram_agree` tinyint(4) NOT NULL DEFAULT 1,
  PRIMARY KEY (`account_uid`),
  UNIQUE KEY `nick_name_UNIQUE` (`nick_name`)
) ENGINE=MyISAM AUTO_INCREMENT=1518 DEFAULT CHARSET=utf8;

/*Table structure for table `tb_arena_normal_hall_of_fame` */

DROP TABLE IF EXISTS `tb_arena_normal_hall_of_fame`;

CREATE TABLE `tb_arena_normal_hall_of_fame` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `rank_list` longtext DEFAULT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=94 DEFAULT CHARSET=utf8;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
