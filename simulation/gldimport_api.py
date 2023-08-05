#import gridlabd_functions
import os
import pandas
import numpy
import random
#import pycurl
from io import StringIO
import json
import gridlabd

import requests

from HH_global import city, market_data, C, interval

#These function descrbe the physical interface: read out of physical environment / API --> provide information / fill into DB

###############
# GENERAL functions for interaction of GLD and py
###############

#Initialization: Find relevant objects and appliances

def find_objects(criteria) :
	finder = criteria.split("=")
	if len(finder) < 2 :
		raise Exception("find(criteria='key=value'): criteria syntax error")
	objects = gridlabd.get("objects")
	result = []
	for name in objects :
		try:
			item = gridlabd.get_object(name)
			if finder[0] in item.keys() and item[finder[0]] == finder[1] :
				result.append(name)
		except:
			pass
	return result

#Get specific object

def get(obj):
	finder = obj.split("=")
	return

###############
# HOUSEHOLDS
###############

#Get house characteristics and write to DB

def get_houseobjects(house_name,time):
	#Get information from physical representation
	house_obj = gridlabd.get_object(house_name) #GUSTAVO: API implementation
	#Switch off default control
	gridlabd.set_value(house_name,'thermostat_control','NONE')
	gridlabd.set_value(house_name,'system_mode','OFF')
	
	#Read out settings
	k = float(house_obj['k'])
	T_max = float(house_obj['T_max'])
	cooling_setpoint = float(house_obj['cooling_setpoint'])
	cooling_demand = float(house_obj['cooling_demand']) #cooling_demand is in kW
	T_min = float(house_obj['T_min'])
	heating_setpoint = float(house_obj['heating_setpoint'])
	heating_demand = float(house_obj['heating_demand']) #heating_demand is in kW

	#Save in long-term memory (in the db) - accessible for market code
	parameter_string = '(timedate, k, T_min, heating_setpoint, T_max, cooling_setpoint)' #timedate TIMESTAMP PRIMARY KEY, 
	value_tuple = (time, k,T_min,heating_setpoint,T_max,cooling_setpoint,)
	myfct.set_values(house_name+'_settings', parameter_string, value_tuple)

	return

def get_PVs(house_name,time):
	#import pdb; pdb.set_trace()
	PV_name = 'PV'+house_name[5:]
	PV_obj = gridlabd.get_object(PV_name)

	#Read out settings
	Q_rated = float(PV_obj['rated_power'])/1000. #kWh

	#Save in long-term memory (in the db) - accessible for market code
	parameter_string = '(timedate, Q_rated)'
	value_tuple = (time, Q_rated,)
	myfct.set_values(PV_name+'_settings', parameter_string, value_tuple)

def get_batteries(house_name,time):
	battery_name = 'Battery'+house_name[5:]
	battery_obj = gridlabd.get_object(battery_name)

	#Read out settings
	SOC_max = float(battery_obj['E_Max'])/1000. #kWh
	soc_min = 0.2 #could be part of user settings
	soc_des = 0.5
	i_max = float(battery_obj['I_Max'].split('+')[1])
	u_max = float(battery_obj['rated_power'])/1000. #kVA
	efficiency = float(battery_obj['round_trip_efficiency'])
	Kes = float(battery_obj['Kes'])

	#Save in long-term memory (in the db) - accessible for market code
	parameter_string = '(timedate, soc_des, soc_min, SOC_max, i_max, u_max, efficiency, Kes)'
	value_tuple = (time, soc_des, soc_min, SOC_max, i_max, u_max, efficiency, Kes,)
	myfct.set_values(battery_name+'_settings', parameter_string, value_tuple)

#This connects to the ChargePoint chargers = an inverter
#No technical information is provided!!
def get_chargers(house_name,time):	
	#Get charger object
	CP_inv_name = 'EV_inverter'+house_name[5:]
	CP_inv_obj = gridlabd.get_object(CP_inv_name)

	#Save in long-term memory (in the db) - accessible for market code
	Qmax = float(CP_inv_obj['rated_power'])
	parameter_string = '(timedate, Qmax, Qset)'
	value_tuple = (time, Qmax, Qmax,) #assume that maximum is allowed
	myfct.set_values('CP'+house_name[5:]+'_settings', parameter_string, value_tuple)

def initialize_EVs(house_name,time):
	#Check if EV is connected
	EV_name = 'EV'+house_name[5:]
	try:
		EV_obj = gridlabd.get_object(EV_name)
		status = True
	except:
		status = False
	if status:
		parameter_string = '(timedate, Kev, tdep, Emax, DeltaE)'
		try:
			Kev = float(EV_obj['Kev'])
		except:
			Kev = 1.0
		try:
			tdep = pandas.to_datetime(EV_obj['tdep'])
		except:
			#Assuming that departure is in the morning
			t0 = pandas.to_datetime(time)
			t0.hours = 0
			tdep = t0 + pandas.Timedelta(hours=0) + pandas.Timedelta(minutes=random.randint(0, 60*1))
			gridlabd.set_value(EV_name,'tdep',str(tdep))
		try:
			Emax = float(EV_obj['battery_capacity'])
		except:
			Emax = 1000.0 #Set very large
		try:
			DeltaE = float(EV_obj['DeltaE'])
		except:
			DeltaE = 100.0 #100% / full charge
		if DeltaE == 0.0:
			DeltaE = 100.0

		value_tuple = (time, str(Kev), str(tdep), Emax, DeltaE,)
		myfct.set_values(EV_name+'_state_in', parameter_string, value_tuple)
	
#Simulates arrival and disconnects EV upon departure - this function should be deleted in physical system
#Therefore also no interaction with DB yet - that's in update_EV_state()
def simulate_EVs(house_name,dt_sim_time):
	EV_name = 'EV'+house_name[5:]
	EV_obj = gridlabd.get_object(EV_name)
	online_t = EV_obj['generator_status']
	CP_inv_name = 'EV_inverter'+house_name[5:]

	if online_t == 'OFFLINE':
		if dt_sim_time.hour >= 0 and dt_sim_time.hour <= 19:
			if arrival := numpy.random.choice(
				[True, False], p=[10 / 60.0, 1.0 - 10 / 60.0]
			):
				#Actual physical parameters
				gridlabd.set_value(EV_name,'generator_status','ONLINE')
				soc = numpy.random.uniform(0.2,0.8)
				gridlabd.set_value(EV_name,'state_of_charge',str(soc)) #Unknow in TESS

				#Settings through User App
				Kev = numpy.random.uniform(0.5,1.5)
				gridlabd.set_value(EV_name,'Kev',str(Kev))
				tdep = dt_sim_time + pandas.Timedelta(hours=7) + pandas.Timedelta(minutes=random.randint(0, 60*1))
				gridlabd.set_value(EV_name,'tdep',str(tdep))
				DeltaE = max(numpy.random.choice(numpy.arange(5.,30.,5.),p=[1/5.]*5),(1.-soc)*100.)
				gridlabd.set_value(EV_name,'DeltaE',str(DeltaE))
				gridlabd.set_value(CP_inv_name,'EV_connected',str(1))				

	elif online_t == 'ONLINE':
		#EV_obj = gridlabd.get_object(EV_name) #get new departure time
		if pandas.to_datetime(EV_obj['tdep']) < dt_sim_time:
			gridlabd.set_value(EV_name,'generator_status','OFFLINE')
			gridlabd.set_value(CP_inv_name,'EV_connected',str(-1))
	#import pdb; pdb.set_trace()

###########################
#
# These functions here describe the writing from HEILA API to the DB
#
###########################

def update_house_state(house_name,dt_sim_time):
	#Get information from physical representation
	house_obj = gridlabd.get_object(house_name)

	#Determine principal mode
	#DAVE: this is a heuristic
	T_air = float(house_obj['air_temperature'])
	if T_air >= (float(house_obj['heating_setpoint']) + float(house_obj['cooling_setpoint']))/2:
		mode = 'COOL'
	else:
		mode = 'HEAT'
	actual_mode = house_obj['system_mode']

	#Save in long-term memory (in the db) - accessible for market code
	parameter_string = '(timedate, mode, actual_mode, T_air, q_heat, q_cool)' #timedate TIMESTAMP PRIMARY KEY, 
	value_tuple = (dt_sim_time, mode, actual_mode, T_air, float(house_obj['heating_demand']),float(house_obj['cooling_demand']),)
	myfct.set_values(house_name+'_state_in', parameter_string, value_tuple)
	return

def update_PV_state(PV_name,dt_sim_time):
	#Get information from physical representation
	PV_obj = gridlabd.get_object(PV_name)

	Qmtp = float(PV_obj['P_Out'][1:].split('+')[0])/1000. #kW
	E = Qmtp/(3600./interval)

	#Save in long-term memory (in the db) - accessible for market code
	parameter_string = '(timedate, E, Qmtp)' #timedate TIMESTAMP PRIMARY KEY, 
	value_tuple = (dt_sim_time, E, Qmtp,)
	myfct.set_values(PV_name+'_state_in', parameter_string, value_tuple)


def update_CP_state(CP_name,dt_sim_time):
	#Check if EV is there
	CP_obj = gridlabd.get_object(CP_name)
	EV_name = 'EV_'+CP_name.split('_')[-1]
	EV_obj = gridlabd.get_object(EV_name)
	#New car arrived
	#import pdb; pdb.set_trace()
	#print(int(CP_obj['EV_connected']))
	if int(CP_obj['EV_connected']) == 1: #This should be whatever signal which pushes the new that a car arrived/disconnected
		#import pdb; pdb.set_trace()
		Kev = float(EV_obj['Kev'])
		tdep = pandas.to_datetime(EV_obj['tdep'])
		Emax = float(EV_obj['battery_capacity'])
		DeltaE = float(EV_obj['DeltaE'])
		#Write to database
		parameter_string = '(timedate, Kev, tdep, Emax, DeltaE)'
		value_tuple = (str(dt_sim_time), str(Kev), str(tdep), Emax, DeltaE,)
		myfct.set_values(EV_name+'_state_in', parameter_string, value_tuple)
		#Reset action pointer
		gridlabd.set_value(CP_name,'EV_connected',str(0))
	elif int(CP_obj['EV_connected']) == -1:
		gridlabd.set_value(CP_name,'EV_connected',str(0))

def update_battery_state(battery_name,dt_sim_time):
	#Get information from physical representation
	batt_obj = gridlabd.get_object(battery_name)

	#Save in long-term memory (in the db) - accessible for market code
	parameter_string = '(timedate, soc_rel)' #timedate TIMESTAMP PRIMARY KEY, 
	value_tuple = (dt_sim_time, float(batt_obj['state_of_charge']),)
	myfct.set_values(battery_name+'_state_in', parameter_string, value_tuple)

def update_EV_state(battery_name,dt_sim_time):
	#Get information from physical representation
	EV_obj = gridlabd.get_object(EV_name)

	#Save in long-term memory (in the db) - accessible for market code
	E = float(EV_obj['state_of_charge'])
# 	treq = 
# trem
# Eest
# Qset
# Qobs


	parameter_string = '(timedate, E, treq, trem, Qset, Qobs)' #timedate TIMESTAMP PRIMARY KEY, 
	value_tuple = (dt_sim_time, E, treq, trem, Qset, Qobs,)
	myfct.set_values(battery_name+'_state_in', parameter_string, value_tuple)

###########################
#
# These functions here describe the implementation of the market results (writing result to state)
#
###########################

def dispatch_PV(PV_name,dt_sim_time):
	df_state_out = myfct.get_values_td(PV_name+'_state_out', begin=dt_sim_time, end=dt_sim_time)
	for ind in df_state_out.index:
		if df_state_out['mode'].loc[ind] == 0:
			print('PV should be disconnected; no action taken')

###############
# Market Operator
###############

#Get supply specifications

def get_slackload(dt_sim_time): #GUSTAVO: this information comes from HCE systems
	load_SLACK = float(gridlabd.get_object('node_149')['measured_real_power'])/1000. #measured_real_power in [W]
	#C - can also come from HCE setting
	myfct.set_values('system_load', '(timedate, C, slack_load)', (dt_sim_time, C, load_SLACK,))
	return

###############
# WHOLESALE SUPPLIER
###############

#This should be coming from HCE's system or other real-time portal

def get_WSprice(dt_sim_time):
	df_WS = pandas.read_csv('glm_generation_'+city+'/'+market_data,parse_dates=[-1],index_col=[0])
	df_WS = pandas.DataFrame(index=pandas.to_datetime(df_WS.index.astype(str)),columns=df_WS.columns,data=df_WS.values.astype(float))
	p_WS = float(df_WS['RT'].loc[dt_sim_time]) 
	myfct.set_values('WS_supply', '(timedate, WS_price)', (dt_sim_time, p_WS,))
	return

###############
# NOT USED
###############

def sort_list(unsorted_list):
	if unsorted_list:
		no = [int(x.split('_')[-1]) for x in unsorted_list]
		d = dict(zip(no,unsorted_list))
		sorted_list = []
		for i in range(1,max(no)+1):
			try:
				sorted_list.append(d[i])
			except:
				pass
	return 

def sort_batteries(batteries):
	batterylist_unsorted = [] #;
	EVlist_unsorted = []

	#Batteries not ordered accoridng to house numbers
	for battery in batteries:
		#name = battery['name']
		#if int(battery['name'].split('_')[-1]) < amount:
		if 'Battery_' in battery:
			batterylist_unsorted.append(battery)
		elif 'EV_' in battery:
			EVlist_unsorted.append(battery)

	batterylist = batterylist_unsorted
	#batterylist = sort_list(batterylist_unsorted)
	EVlist = EVlist_unsorted
	#EVlist = sort_list(EVlist_unsorted)

	return batterylist, EVlist

def sort_pvs(pvs):
	#Sort PVs

	pv_list = []
	if pvlist_unsorted := list(pvs):
		pvlist_no = [int(x.split('_')[-1]) for x in pvlist_unsorted]
		d = dict(zip(pvlist_no,pvlist_unsorted))
		for i in range(1,max(pvlist_no)+1):
			try:
				pv_list.append(d[i])
			except:
				pass

	pvinv_list = ['PV_inverter_' + pv[3:] for pv in pv_list]
	return pv_list, pvinv_list