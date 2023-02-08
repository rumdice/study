rsync -avz -e ssh gameserver/src owl@192.168.0.6:/home/owl/owlserver/gameserver
rsync -avz -e ssh gameserver/guild_raid_reward_scheduler_dev.py owl@192.168.0.6:/home/owl/owlserver/gameserver
rsync -avz -e ssh gameserver/gamedata owl@192.168.0.6:/home/owl/owlserver/gameserver
ssh owl@192.168.0.6 "~/owlserver/reload_server.sh"

