rsync -avz -e ssh gameserver/src owl@192.168.0.7:/home/owl/jenkins/owlserver/gameserver
rsync -avz -e ssh gameserver/guild_raid_reward_scheduler_dev.py owl@192.168.0.7:/home/owl/jenkins/owlserver/gameserver
rsync -avz -e ssh gameserver/gamedata owl@192.168.0.7:/home/owl/jenkins/owlserver/gameserver
ssh owl@192.168.0.7 "~/reload_rp_server.sh"

