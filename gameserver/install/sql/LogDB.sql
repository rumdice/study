-- MySQL dump 10.13  Distrib 5.5.62, for Win64 (AMD64)
--
-- Host: localhost    Database: LogDB
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
-- Table structure for table `tb_adventure_log`
--

DROP TABLE IF EXISTS `tb_adventure_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_adventure_log` (
  `uid` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `log_time` datetime NOT NULL,
  `auid` int(10) unsigned NOT NULL,
  `log_type` int(10) unsigned NOT NULL,
  `value1` int(10) unsigned NOT NULL,
  `value2` int(10) unsigned NOT NULL,
  `reward_list` longtext NOT NULL,
  PRIMARY KEY (`uid`,`log_time`),
  KEY `auid_index` (`auid`)
) ENGINE=MyISAM AUTO_INCREMENT=2388 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_equip_enchant_log`
--

DROP TABLE IF EXISTS `tb_equip_enchant_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_equip_enchant_log` (
  `uid` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `log_time` datetime NOT NULL,
  `auid` int(10) unsigned NOT NULL,
  `item_uid` int(10) unsigned NOT NULL,
  `item_id` int(11) NOT NULL,
  `befor_exp` int(11) NOT NULL,
  `after_exp` int(11) NOT NULL,
  `material_list` longtext NOT NULL,
  PRIMARY KEY (`uid`),
  KEY `auid_idx` (`auid`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_event_dungeon_log`
--

DROP TABLE IF EXISTS `tb_event_dungeon_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_event_dungeon_log` (
  `uid` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `log_time` datetime NOT NULL,
  `auid` int(10) unsigned NOT NULL,
  `log_type` int(11) NOT NULL,
  `dungeon_uid` int(11) NOT NULL,
  `dungeon_type` int(11) NOT NULL,
  `dungeon_id` int(11) NOT NULL,
  `param1` int(11) NOT NULL,
  `param2` int(11) NOT NULL,
  `reward_list` longtext NOT NULL,
  PRIMARY KEY (`uid`),
  KEY `auid_idx` (`auid`)
) ENGINE=MyISAM AUTO_INCREMENT=512 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_gacha_log`
--

DROP TABLE IF EXISTS `tb_gacha_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_gacha_log` (
  `uid` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `log_time` datetime NOT NULL,
  `auid` int(10) unsigned NOT NULL,
  `gacha_id` int(11) NOT NULL,
  `use_list` longtext NOT NULL,
  `reward_list` longtext NOT NULL,
  PRIMARY KEY (`uid`),
  KEY `auid_idx` (`auid`)
) ENGINE=MyISAM AUTO_INCREMENT=295 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_goods_log`
--

DROP TABLE IF EXISTS `tb_goods_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_goods_log` (
  `uid` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `log_time` datetime NOT NULL,
  `auid` int(10) unsigned NOT NULL,
  `item_id` int(11) NOT NULL,
  `log_type` int(11) NOT NULL,
  `content_type` int(11) NOT NULL,
  `value` int(11) NOT NULL,
  `cost` int(11) NOT NULL,
  `result` int(11) NOT NULL,
  `content_uid` bigint(20) unsigned NOT NULL,
  PRIMARY KEY (`uid`),
  KEY `auid_idx` (`auid`)
) ENGINE=MyISAM AUTO_INCREMENT=16338 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_hero_levelup`
--

DROP TABLE IF EXISTS `tb_hero_levelup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_hero_levelup` (
  `uid` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `log_time` datetime NOT NULL,
  `log_type` int(11) NOT NULL,
  `auid` int(10) unsigned NOT NULL,
  `item_uid` int(10) unsigned NOT NULL,
  `item_id` int(11) NOT NULL,
  `befor_value` int(11) NOT NULL,
  `after_value` int(11) NOT NULL,
  `material_list` longtext NOT NULL,
  PRIMARY KEY (`uid`),
  KEY `auid_index` (`auid`)
) ENGINE=MyISAM AUTO_INCREMENT=2187 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_hero_return_log`
--

DROP TABLE IF EXISTS `tb_hero_return_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_hero_return_log` (
  `uid` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `log_time` datetime NOT NULL,
  `auid` int(10) unsigned NOT NULL,
  `material_list` longtext NOT NULL,
  `return_point` int(11) NOT NULL,
  PRIMARY KEY (`uid`),
  KEY `auid_idx` (`auid`)
) ENGINE=MyISAM AUTO_INCREMENT=49 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_item_log`
--

DROP TABLE IF EXISTS `tb_item_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_item_log` (
  `uid` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `log_time` datetime NOT NULL,
  `auid` int(10) unsigned NOT NULL,
  `log_type` int(10) unsigned DEFAULT NULL,
  `content_type` int(11) NOT NULL,
  `item_uid` int(10) unsigned NOT NULL,
  `item_id` int(11) NOT NULL,
  `content_uid` bigint(20) unsigned NOT NULL,
  PRIMARY KEY (`uid`),
  KEY `auid_index` (`auid`)
) ENGINE=MyISAM AUTO_INCREMENT=2767 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_make_item_log`
--

DROP TABLE IF EXISTS `tb_make_item_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_make_item_log` (
  `uid` bigint(20) NOT NULL AUTO_INCREMENT,
  `log_time` datetime NOT NULL,
  `auid` int(10) unsigned NOT NULL,
  `log_type` int(11) NOT NULL,
  `building_slot` int(11) NOT NULL,
  `make_item` int(11) NOT NULL,
  `material_list` longtext NOT NULL,
  PRIMARY KEY (`uid`),
  KEY `auid_idx` (`auid`)
) ENGINE=MyISAM AUTO_INCREMENT=169 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_resource_camp_log`
--

DROP TABLE IF EXISTS `tb_resource_camp_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_resource_camp_log` (
  `uid` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `log_time` datetime NOT NULL,
  `log_type` int(11) NOT NULL,
  `auid` int(10) unsigned NOT NULL,
  `camp_item` int(11) NOT NULL,
  `camp_lv` int(11) NOT NULL,
  `distance` int(11) NOT NULL,
  `data_list` longtext NOT NULL,
  PRIMARY KEY (`uid`),
  KEY `auid_idx` (`auid`)
) ENGINE=MyISAM AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_territory_build_log`
--

DROP TABLE IF EXISTS `tb_territory_build_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_territory_build_log` (
  `uid` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `log_time` datetime NOT NULL,
  `auid` int(10) unsigned NOT NULL,
  `building_type` int(11) NOT NULL,
  `level` int(11) NOT NULL,
  `build_slot` int(11) NOT NULL,
  `material_list` longtext NOT NULL,
  PRIMARY KEY (`uid`),
  KEY `auid_idx` (`auid`)
) ENGINE=MyISAM AUTO_INCREMENT=1701 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_trade_log`
--

DROP TABLE IF EXISTS `tb_trade_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_trade_log` (
  `uid` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `log_time` datetime NOT NULL,
  `auid` int(10) unsigned NOT NULL,
  `product_info` longtext NOT NULL,
  `purchase_info` longtext NOT NULL,
  PRIMARY KEY (`uid`),
  KEY `auid_idx` (`auid`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping routines for database 'LogDB'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-07-14 15:18:55
