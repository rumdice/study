/*
SQLyog Community v13.1.9 (64 bit)
MySQL - 10.5.8-MariaDB-1:10.5.8+maria~focal : Database - db_game
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`db_game` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci */;

USE `db_game`;

/*Table structure for table `tb_deck` */

DROP TABLE IF EXISTS `tb_deck`;

CREATE TABLE `tb_deck` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `auid` int(10) NOT NULL,
  `formation` int(10) NOT NULL,
  `huid1` int(10) DEFAULT NULL,
  `huid2` int(10) DEFAULT NULL,
  `huid3` int(10) DEFAULT NULL,
  `huid4` int(10) DEFAULT NULL,
  `huid5` int(10) DEFAULT NULL,
  `h1_euid1` int(10) DEFAULT NULL,
  `h1_euid2` int(10) DEFAULT NULL,
  `h2_euid1` int(10) DEFAULT NULL,
  `h2_euid2` int(10) DEFAULT NULL,
  `h3_euid1` int(10) DEFAULT NULL,
  `h3_euid2` int(10) DEFAULT NULL,
  `h4_euid1` int(10) DEFAULT NULL,
  `h4_euid2` int(10) DEFAULT NULL,
  `h5_euid1` int(10) DEFAULT NULL,
  `h5_euid2` int(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`auid`,`formation`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
