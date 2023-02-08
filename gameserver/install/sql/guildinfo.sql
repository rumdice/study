-- MySQL dump 10.13  Distrib 5.5.62, for Win64 (AMD64)
--
-- Host: localhost    Database: guildinfodb
-- ------------------------------------------------------
-- Server version	5.5.5-10.5.8-MariaDB-1:10.5.8+maria~focal

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `tb_guildInfo`
--

DROP TABLE IF EXISTS `tb_guildInfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_guildInfo` (
  `guild_uid` int(11) NOT NULL,
  `guild_point` int(11) DEFAULT NULL,
  `member_count` int(11) DEFAULT NULL,
  `join_level` int(11) DEFAULT NULL,
  `join_type` int(11) DEFAULT NULL,
  `guild_msg` varchar(255) DEFAULT NULL,
  `raid_monster` int(11) DEFAULT 0,
  `raid_element` int(11) DEFAULT 0,
  `raid_monster_hp` int(11) DEFAULT 0,
  `raid_monster_level` int(11) DEFAULT 0,
  `raid_complete_count` int(11) DEFAULT 0,
  `contest_enemy_guild_guid` int(11) DEFAULT NULL,
  `contest_monster` int(11) DEFAULT 0,
  `contest_element` int(11) DEFAULT 0,
  `contest_monster_hp` int(11) DEFAULT 0,
  `contest_monster_level` int(11) DEFAULT 0,
  `contest_complete_count` int(11) DEFAULT 0,
  PRIMARY KEY (`guild_uid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_guild_member`
--

DROP TABLE IF EXISTS `tb_guild_member`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_guild_member` (
  `guild_uid` int(10) unsigned NOT NULL,
  `auid` int(10) unsigned NOT NULL,
  `guild_grade` int(10) unsigned DEFAULT NULL,
  `raid_start_time` datetime DEFAULT NULL,
  `raid_record` longtext DEFAULT NULL,
  `reward_grade` int(11) DEFAULT 0,
  `reward_damage` int(11) DEFAULT 0,
  `reward_flag` tinyint(4) DEFAULT 0,
  PRIMARY KEY (`auid`),
  KEY `uid` (`guild_uid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_guild_raid_damage`
--

DROP TABLE IF EXISTS `tb_guild_raid_damage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_guild_raid_damage` (
  `guild_uid` int(11) NOT NULL,
  `auid` int(11) NOT NULL,
  `total_damage` int(11) NOT NULL,
  PRIMARY KEY (`auid`,`guild_uid`),
  KEY `guild_idx` (`guild_uid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_raid_result`
--

DROP TABLE IF EXISTS `tb_raid_result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_raid_result` (
  `guild_uid` int(11) NOT NULL,
  `raid_monster` int(11) DEFAULT 0,
  `element` int(11) DEFAULT 0,
  `monster_hp` int(11) DEFAULT 0,
  `monster_level` int(11) DEFAULT 0,
  `damage_record` longtext DEFAULT NULL,
  PRIMARY KEY (`guild_uid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping routines for database 'guildinfodb'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-07-14 15:18:56
