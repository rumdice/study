# -*- coding: utf-8 -*-
import os
import random

from src.context import *
from src.services.service_common import *
from src.tables.table_Base import *

# 매치메이킹 서버 직접 실행 :
# 해당 스크립트를 서버 webapp.py와 같은 경로에 복사하여 python 가상환경 진입 후 직접 실행.
# source /venv/bin/activate
# python _contest_match.py

# 운영툴에 길드 승부 매치하기 기능 이관 완료.
# 운영툴을 셋팅하고 길드승부 0일째 이걸 한번만 돌리면 된다.

# - 운영툴에 기능으로 넣기. (기간셋팅) -> 0일날 스크립트 실행.
# 길드 승부 상대방 길드를 찾아서 db에 넣어줘서 메치되게 해주는 기능
# 운영툴로 기능 제공 전까지는 개발자가 직접 실행
# 기획서상 길드 승부 시작 시간 후 0일차 동안 유저가 직접 실행하여 서로 매칭을 잡아주는걸 강제로 빠르게 잡아주는 스크립트

# 일단 개발중 급하니까 개발서버에서 서버 개발자가 가상환경 진입후 이 파이썬 코드 직접 실행하여 매칭을 다 잡아 준다
# 0일차 동안 진행되는 매칭이 다 잡힘
# gameserver 폴더로 이동 후
# source bin/venv/activate
# python _match.py
# 매칭 잡힌거 db에서 확인하기 (db_guild/tb_guildinfo 테이블)

# 이 스크립트를 실행하면 매칭이 전부 잡히므로 0일차가 지나간 효과를 낸다.(강제로 0일차가 지난 효과)
# 즉 운영툴에서 길드 승부 기간을 2023-01-08 00:00:00 / 2023-01-11 00:00:00 로 잡았다면 (0일차 ~ 3일차)
# 길드 승부 기간을 2023-01-07 00:00:00 / 2023-01-10 00:00:00 로 하루 땡겨야 게임서버 로직에 맞게 동작한다.
# (현재시간 1월 8일 기준) 0일차를 그냥 보냈으므로 하루 땡기는거다. 

# 특이사항
# war_point (guild_point)는 현재 무시한 상태로 매칭을 잡아준다. - 임의의 값을 넣어 줄 것 (200)
# 차후 길드전 등에서 해당 값이 사용될 예정.


def create_guild_contest_monster_level(self, guild_point1, guild_point2):
    avg_point = (guild_point1 + guild_point2) / 2
    for item in self.table.contest:
        if item.point_min <= avg_point and avg_point <= item.point_max:
            return item.monster_level
    return 1

def create_guild_contest_monster_id(self):
    key = random.choice(list(self.table.contest_monster.keys()))
    boss_info = self.table.contest_monster[key][0]
    mob_id = boss_info['mob_id']
    return mob_id


class ContestMatchService():
    def __init__(self, context):
        self.context = context
        self.table = TableBase()
        self.w_db = context.w_db

    def contest_matchmaking(self):
        print("guild contest match start")

        db_guildcontestinfo = self.w_db['guildcontestinfo'].get_guild_contest_info()
        if not db_guildcontestinfo:
            print("None db_guildcontestinfo")
            return

        guildList = self.w_db['guildinfo'].get_guild_all()
        guildList.sort(key = lambda x:-x[1])

        matchList = []
        variant = [30, 60, 150, 300]
    
        for guild in guildList:
            if guild not in matchList:
                for var in variant:
                    targetCount = var
                    max = guild.guild_point + targetCount
                    min = guild.guild_point - targetCount

                    rangeList = [x for x in guildList if x.guild_point < max and x not in matchList][:10]
                    rangeList += [x for x in guildList if x.guild_point > min and x not in matchList]
                    
                    tempList = []
                    [tempList.append(x) for x in rangeList if x not in tempList and x != guild]
                    
                    if len(tempList) <= 0 :
                        print("len:", len(tempList))
                        break

                    matchtarget = random.choice(tempList)
                    if matchtarget:
                        print("guild: {} <-> target: {}".format(guild.guild_uid, matchtarget.guild_uid))
                        matchList.append(guild)
                        matchList.append(matchtarget)
                        break
            else:
                pass

        for i, player in enumerate(matchList):
            is_even = True if i % 2 == 0 else False
            enemy = matchList[i + 1] if is_even else matchList[int(i / 2) * 2]
            enemy_guild_uid = enemy.guild_uid
            
            # enemy_guild_point = enemy.guild_point
            # player_guild_point = player.guild_point
            # TODO: 길드 포인트 (워포인트) 임의 값 - 차후 다양한 컨텐츠에서 이 값을 조절함. 200 기준으로 매칭셋팅하므로 몬스터 렙은 20
            enemy_guild_point = 200
            player_guild_point = 250
        
            contest_monster_level = create_guild_contest_monster_level(self, player_guild_point, enemy_guild_point)
            contest_monster = create_guild_contest_monster_id(self)
            boss_data = self.table.hero.get(contest_monster, None)
            contest_monster_hp = boss_data.hp
            contest_complete_count = 0
            contest_element = 1

            self.w_db['guildinfo'].update_contest_enemy_guild(
                guild_uid=player.guild_uid,
                enemy_guild_uid=enemy_guild_uid,
                contest_monster=contest_monster,
                contest_element=contest_element,
                contest_monster_hp=contest_monster_hp,
                contest_monster_level=contest_monster_level,
                contest_complete_count=contest_complete_count
            )

        print("guild contest match complete")

conf_dir = os.path.dirname(os.path.abspath(__file__)) + "/conf/"
service_ini = conf_dir + "service_local.ini"

if __name__ == '__main__':
    context = GameServerContext(
        inifile=service_ini,
        after_init=init_callback
    )

    service = ContestMatchService(context)
    service.contest_matchmaking()
    pass

