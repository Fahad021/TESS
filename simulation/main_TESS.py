import gridlabd
import pandas as pd
import time
from datetime import date
import requests

from HH_global import start_time_str, end_time_str
from HH_global import db_address #, user_name, pw

# Mysql - manually delete interval data

# mysql -u root -p pw
# DELETE FROM tess.market_intervals;
# DELETE FROM tess.meter_intervals;
# exit;

#Rewrite players to today's day

# import os
# player_path = 'glm_generation_Austin/players_Austin'
# players = os.listdir(player_path)
# for player in players:
# 	if '.player' in player:
# 		original_player = open(player_path + ' copy/' + player, "r")
# 		#player = open(player_path + '/' + player, "w+").close()
# 		player = open(player_path + '/' + player, "w+")
# 		first_line = True
# 		for line in original_player:
# 			if first_line:
# 				new_line = str(date.today()) + ' 00:00:00,' + line.split(',')[1]
# 				player.write(new_line)
# 				first_line = False
# 			else:
# 				player.write(line)

#Re-write glm model to today's date

# config_path = 'config'
# original_default = open(config_path + '/default copy.glm', "r")
# #default = open(config_path + '/default.glm', "w+").close()
# default = open(config_path + '/default.glm', "w+")
# for line in original_default:
# 	print(line)
# 	if 'STARTTIME' in line:
# 		default.write('#define STARTTIME=${STARTTIME:-' + str(date.today()) + ' 00:00:00}\n')
# 	elif 'STOPTIME' in line:
# 		default.write('#define STOPTIME=${STOPTIME:-' + str(date.today() + pd.Timedelta(days=1)) + ' 00:00:00}')
# 	else:
# 		default.write(line)
# default.close()

import pdb
pdb.set_trace()

# Adjust/Re-write

# folders
# interval (interval for markets should be identical with recorders)

#Start simulation

gridlabd.command('model_RT.glm')
#gridlabd.command('-D')
#gridlabd.command('run_realtime=TRUE') # CHECK - locks in clock with real-time