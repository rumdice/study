ALTER TABLE `db_game`.`tb_event_dungeon` CHANGE `param1` `param1` INT(10) UNSIGNED DEFAULT 0 NOT NULL, CHANGE `param2` `param2` INT(10) UNSIGNED DEFAULT 0 NOT NULL, CHANGE `param3` `param3` INT(10) UNSIGNED DEFAULT 0 NOT NULL, CHANGE `reward_value` `reward_value` INT(10) UNSIGNED DEFAULT 0 NOT NULL; 


ALTER TABLE `db_game`.`tb_region_info` CHANGE `region_num` `region_num` INT(10) UNSIGNED DEFAULT 0 NOT NULL, CHANGE `region_difficulty` `region_difficulty` INT(10) UNSIGNED DEFAULT 0 NOT NULL, CHANGE `region_step` `region_step` INT(10) UNSIGNED DEFAULT 0 NOT NULL; 


ALTER TABLE `db_game`.`tb_resource_collect` CHANGE `resource_id` `resource_id` INT(11) DEFAULT 0 NOT NULL, CHANGE `resource_lv` `resource_lv` INT(11) DEFAULT 0 NOT NULL, CHANGE `distance` `distance` INT(11) DEFAULT 0 NOT NULL, CHANGE `resource_max` `resource_max` INT(11) DEFAULT 0 NOT NULL, CHANGE `move_time` `move_time` INT(11) DEFAULT 0 NOT NULL; 


ALTER TABLE `db_game`.`tb_profile` DROP COLUMN `etc_inven_max`; 

ALTER TABLE `db_guild`.`tb_guildinfo` CHANGE `guild_point` `guild_point` INT(11) DEFAULT 0 NOT NULL, CHANGE `member_count` `member_count` INT(11) DEFAULT 1 NOT NULL; 


ALTER TABLE `db_guild`.`tb_guildinfo` CHANGE `raid_monster_level` `raid_monster_level` INT(11) DEFAULT 1 NULL; 


ALTER TABLE `db_game`.`tb_inven_hero` ADD COLUMN `potential_stat_list` LONGTEXT NULL AFTER `passive_skill_id2`; 



-- 지역 미션 저장 테이블 관련 테이블 스키마 및 인덱싱 변경
ALTER TABLE `db_game`.`tb_region_mission` ADD COLUMN `id` INT(10) NOT NULL AUTO_INCREMENT FIRST, DROP PRIMARY KEY, ADD PRIMARY KEY (`id`, `region_id`, `difficulty`); 
ALTER TABLE `db_game`.`tb_region_mission` DROP INDEX `auid_idx`, DROP PRIMARY KEY, ADD PRIMARY KEY (`id`), ADD UNIQUE INDEX `search_key` (`auid` , `region_id` , `difficulty`); 



-- 아레나 리펙토링 관련 영웅 인벤 정보 테이블 구조 변경
ALTER TABLE `db_game`.`tb_inven_hero` ADD COLUMN `equip_uid1` INT(10) UNSIGNED NULL AFTER `potential_stat_list`, ADD COLUMN `equip_uid2` INT(10) UNSIGNED NULL AFTER `equip_uid1`; 

-- 아레나 리펙토링 관련 아레나 일반전 테이블 구조 변경
ALTER TABLE `db_game`.`tb_arena_normal` DROP COLUMN `is_battle`;
ALTER TABLE `db_game`.`tb_arena_normal` DROP COLUMN `attack_flag`; 
ALTER TABLE `db_game`.`tb_arena_normal` DROP COLUMN `season_rank`; 