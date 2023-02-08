-- MySQL dump 10.13  Distrib 5.5.62, for Win64 (AMD64)
--
-- Host: localhost    Database: gamedb
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
-- Table structure for table `tb_arena_normal`
--

DROP TABLE IF EXISTS `tb_arena_normal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_arena_normal` (
  `auid` int(10) unsigned NOT NULL,
  `rank` int(11) DEFAULT 0,
  `refresh_time` datetime DEFAULT NULL,
  `target_list` longtext DEFAULT NULL,
  `battle_record` longtext DEFAULT NULL,
  `battle_target_uid` int(10) unsigned DEFAULT 0,
  `battle_start_time` datetime DEFAULT NULL,
  `reward_time` datetime DEFAULT NULL,
  PRIMARY KEY (`auid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_arena_tournament`
--

DROP TABLE IF EXISTS `tb_arena_tournament`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_arena_tournament` (
  `auid` int(10) unsigned NOT NULL,
  `group` int(10) unsigned NOT NULL,
  `target_auid` int(10) unsigned NOT NULL,
  `match_index` int(10) unsigned NOT NULL,
  `battle_count` int(10) unsigned NOT NULL,
  `point` int(10) unsigned NOT NULL,
  `battle_turn` int(10) unsigned NOT NULL,
  `round` int(10) unsigned NOT NULL,
  `reward_rank` int(10) unsigned NOT NULL DEFAULT 0,
  `end_flag` tinyint(4) NOT NULL DEFAULT 0,
  PRIMARY KEY (`auid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_attendance`
--

DROP TABLE IF EXISTS `tb_attendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_attendance` (
  `auid` int(10) unsigned NOT NULL,
  `attend_cnt` int(11) NOT NULL DEFAULT 0,
  `attend_reward_date` datetime DEFAULT NULL,
  `attend_end_date` datetime DEFAULT NULL,
  `event_attend` int(11) DEFAULT 0,
  `event_reward_date` datetime DEFAULT NULL,
  `event_end_date` datetime DEFAULT NULL,
  PRIMARY KEY (`auid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_darknest`
--

DROP TABLE IF EXISTS `tb_darknest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_darknest` (
  `auid` int(10) unsigned NOT NULL,
  `boss_id` int(10) unsigned NOT NULL,
  `respawn_time` datetime DEFAULT NULL,
  `boss_infos` longtext NOT NULL,
  `last_clear` tinyint(4) DEFAULT 0,
  PRIMARY KEY (`auid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_endless_tower`
--

DROP TABLE IF EXISTS `tb_endless_tower`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_endless_tower` (
  `auid` int(10) unsigned NOT NULL,
  `end_time` datetime DEFAULT NULL,
  `clear_floor` int(10) unsigned NOT NULL DEFAULT 0,
  KEY `auid_idx` (`auid`) USING BTREE
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_event_dungeon`
--

DROP TABLE IF EXISTS `tb_event_dungeon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_event_dungeon` (
  `auid` int(10) unsigned NOT NULL,
  `dungeon_uid` int(10) unsigned NOT NULL,
  `dungeon_id` int(10) unsigned NOT NULL,
  `dungeon_type` int(10) unsigned NOT NULL,
  `param1` int(10) unsigned NOT NULL,
  `param2` int(10) unsigned NOT NULL,
  `param3` int(10) unsigned NOT NULL,
  `reward_value` int(10) unsigned NOT NULL,
  `end_time` datetime DEFAULT NULL,
  `use_ids` longtext DEFAULT NULL,
  PRIMARY KEY (`auid`,`dungeon_uid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_farming_tower`
--

DROP TABLE IF EXISTS `tb_farming_tower`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_farming_tower` (
  `auid` int(10) unsigned NOT NULL,
  `tower_uid` int(10) unsigned NOT NULL,
  `tower_id` int(10) unsigned NOT NULL,
  `end_time` datetime DEFAULT NULL,
  `clear_floor` int(10) unsigned NOT NULL DEFAULT 0,
  PRIMARY KEY (`auid`,`tower_uid`),
  KEY `auid_idx` (`auid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_gacha`
--

DROP TABLE IF EXISTS `tb_gacha`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_gacha` (
  `auid` int(10) unsigned NOT NULL,
  `gacha_id` int(11) NOT NULL,
  `summon_time` datetime NOT NULL,
  PRIMARY KEY (`auid`,`gacha_id`),
  KEY `auid` (`auid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_inven_equip`
--

DROP TABLE IF EXISTS `tb_inven_equip`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_inven_equip` (
  `uid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `auid` int(10) unsigned NOT NULL,
  `item_id` int(10) unsigned NOT NULL,
  `inven_type` int(10) unsigned NOT NULL,
  `exp` int(10) unsigned NOT NULL DEFAULT 0,
  `lock_flag` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`uid`),
  KEY `auid_index` (`auid`)
) ENGINE=MyISAM AUTO_INCREMENT=358 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_inven_etc`
--

DROP TABLE IF EXISTS `tb_inven_etc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_inven_etc` (
  `auid` int(10) unsigned NOT NULL,
  `item_id` int(10) unsigned NOT NULL,
  `item_count` int(10) unsigned NOT NULL DEFAULT 1,
  PRIMARY KEY (`auid`,`item_id`),
  KEY `auid_index` (`auid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_inven_hero`
--

DROP TABLE IF EXISTS `tb_inven_hero`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_inven_hero` (
  `uid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `auid` int(10) unsigned NOT NULL,
  `item_id` int(10) unsigned NOT NULL,
  `tier` int(10) unsigned NOT NULL DEFAULT 1,
  `exp` int(10) unsigned NOT NULL DEFAULT 0,
  `dispatch_flag` tinyint(1) DEFAULT 0,
  `lock_flag` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`uid`),
  KEY `auid_index` (`auid`)
) ENGINE=MyISAM AUTO_INCREMENT=2451 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_make_item`
--

DROP TABLE IF EXISTS `tb_make_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_make_item` (
  `auid` int(10) unsigned NOT NULL,
  `building_uid` int(10) unsigned NOT NULL,
  `make_itemid0` int(11) DEFAULT 0,
  `end_time0` datetime DEFAULT current_timestamp(),
  `make_itemid1` int(11) DEFAULT 0,
  `end_time1` datetime DEFAULT current_timestamp(),
  `make_itemid2` int(11) DEFAULT 0,
  `end_time2` datetime DEFAULT current_timestamp(),
  `make_itemid3` int(11) DEFAULT 0,
  `end_time3` datetime DEFAULT current_timestamp(),
  `make_itemid4` int(11) DEFAULT 0,
  `end_time4` datetime DEFAULT current_timestamp(),
  `make_itemid5` int(11) DEFAULT 0,
  `end_time5` datetime DEFAULT current_timestamp(),
  `make_itemid6` int(11) DEFAULT 0,
  `end_time6` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`auid`,`building_uid`),
  KEY `auid` (`auid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_post`
--

DROP TABLE IF EXISTS `tb_post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_post` (
  `post_uid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `auid` int(10) unsigned NOT NULL,
  `post_type` int(11) NOT NULL,
  `title_msg` varchar(45) NOT NULL,
  `post_msg` varchar(255) NOT NULL,
  `post_item` longtext NOT NULL,
  `read_flag` tinyint(4) NOT NULL DEFAULT 0,
  `remove_time` datetime NOT NULL,
  `reward_flag` tinyint(4) NOT NULL DEFAULT 0,
  `keep_day` int(11) NOT NULL DEFAULT 1,
  PRIMARY KEY (`post_uid`),
  KEY `auid_idx` (`auid`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_profile`
--

DROP TABLE IF EXISTS `tb_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_profile` (
  `auid` int(10) unsigned NOT NULL,
  `avatar_id` int(10) unsigned NOT NULL DEFAULT 0,
  `level` int(10) unsigned NOT NULL DEFAULT 1,
  `exp` int(10) unsigned NOT NULL DEFAULT 0,
  `equip_normal_inven_max` int(10) unsigned NOT NULL,
  `equip_pvp_inven_max` int(10) unsigned NOT NULL,
  `etc_inven_max` int(10) unsigned NOT NULL,
  `hero_inven_max` int(10) unsigned NOT NULL,
  `cash` int(10) unsigned NOT NULL DEFAULT 0,
  `money` int(10) unsigned NOT NULL DEFAULT 0,
  `stamina_max` int(10) unsigned NOT NULL DEFAULT 0,
  `stamina_cur` int(10) unsigned NOT NULL DEFAULT 0,
  `stamina_time` datetime DEFAULT current_timestamp(),
  `guild_point` int(11) NOT NULL DEFAULT 0,
  `guild_uid` int(11) NOT NULL DEFAULT 0,
  `guild_withdraw_time` datetime DEFAULT NULL,
  `guild_raid_ticket` int(10) unsigned DEFAULT NULL,
  `guild_raid_ticket_time` datetime DEFAULT current_timestamp(),
  `last_mode` int(11) DEFAULT 0,
  `last_stage` int(11) DEFAULT 0,
  `arena_ticket` int(10) unsigned DEFAULT NULL,
  `arena_ticket_time` datetime DEFAULT current_timestamp(),
  `darknest_ticket` int(10) unsigned NOT NULL,
  `darknest_ticket_time` datetime DEFAULT current_timestamp(),
  `arena_match_refresh_time` datetime DEFAULT NULL,
  `guild_contest_ticket` int(10) unsigned DEFAULT NULL,
  `guild_contest_ticket_time` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`auid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_region_info`
--

DROP TABLE IF EXISTS `tb_region_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_region_info` (
  `auid` int(10) unsigned NOT NULL,
  `region_num` int(10) unsigned NOT NULL,
  `region_difficulty` int(10) unsigned NOT NULL,
  `region_step` int(10) unsigned NOT NULL,
  PRIMARY KEY (`auid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_region_mission`
--

DROP TABLE IF EXISTS `tb_region_mission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_region_mission` (
  `auid` int(10) unsigned NOT NULL,
  `region_id` int(11) NOT NULL,
  `difficulty` int(11) NOT NULL,
  `reward_list` longtext NOT NULL,
  PRIMARY KEY (`auid`,`region_id`,`difficulty`),
  KEY `auid_idx` (`auid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_resource_collect`
--

DROP TABLE IF EXISTS `tb_resource_collect`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_resource_collect` (
  `auid` int(10) unsigned NOT NULL,
  `resource_idx` int(11) NOT NULL,
  `resource_id` int(11) NOT NULL,
  `resource_lv` int(11) NOT NULL,
  `distance` int(11) NOT NULL,
  `dispatch_list` longtext NOT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `resource_max` int(11) NOT NULL,
  `move_time` int(11) NOT NULL,
  PRIMARY KEY (`auid`,`resource_idx`),
  KEY `auid_idx` (`auid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_resource_dispatch`
--

DROP TABLE IF EXISTS `tb_resource_dispatch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_resource_dispatch` (
  `auid` int(10) unsigned NOT NULL,
  `resource_idx` int(11) NOT NULL,
  `resource_id` int(11) NOT NULL,
  `resource_lv` int(11) NOT NULL,
  `distance` int(11) NOT NULL,
  PRIMARY KEY (`auid`,`resource_idx`),
  KEY `auid_idx` (`auid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_territory`
--

DROP TABLE IF EXISTS `tb_territory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_territory` (
  `uid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `auid` int(10) unsigned NOT NULL,
  `building_type` int(11) NOT NULL,
  `level` int(11) NOT NULL,
  `start_time` datetime DEFAULT NULL,
  `build_slot` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`uid`),
  KEY `auid_idx` (`auid`)
) ENGINE=MyISAM AUTO_INCREMENT=479 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_territory_build`
--

DROP TABLE IF EXISTS `tb_territory_build`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_territory_build` (
  `uid` int(10) unsigned NOT NULL,
  `auid` int(10) unsigned NOT NULL,
  `building_type` int(11) NOT NULL,
  `build_level` int(11) NOT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`uid`),
  KEY `auid_idx` (`auid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_tradeItem`
--

DROP TABLE IF EXISTS `tb_tradeItem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_tradeItem` (
  `auid` int(10) unsigned NOT NULL,
  `building_uid` int(10) unsigned NOT NULL,
  `trade_item1` longtext DEFAULT NULL,
  `trade_item2` longtext DEFAULT NULL,
  `trade_item3` longtext DEFAULT NULL,
  `trade_item4` longtext DEFAULT NULL,
  `refresh_time` datetime DEFAULT NULL,
  PRIMARY KEY (`auid`,`building_uid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping routines for database 'gamedb'
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
