# This file populates the db with customers and PV panels (and all other necessary dependencies)

import gridlabd
import pandas as pd
import time
from datetime import date
import requests

from HH_global import start_time_str, end_time_str
from HH_global import db_address #, user_name, pw

# Reminder for cleaning up data
# Mysql - manually delete interval data

# mysql -u root -p pw
# DELETE FROM tess.market_intervals;
# DELETE FROM tess.meter_intervals;
# exit;

# Number of customers

no_users = 6

#Set up market

data = {'source': 'Ercot', 'ts': 5, 'p_max': 10000}
market = requests.post(db_address+'market',json=data,auth=(user_name,pw))
#market = requests.get(db_address+'markets').json()
#Set up utility
data = {'name':'HCE','subscription_start':str(pd.Timestamp(start_time_str)),'subscription_end':str(pd.Timestamp(end_time_str))}
requests.post(db_address+'utility',json=data,auth=(user_name,pw))
#utility = requests.get(db_address+'utilities').json()
#Set up rate
data = {'description':'net_metering'}
requests.post(db_address+'rate',json=data,auth=(user_name,pw))
#rate = requests.get(db_address+'rates').json()
#Set up transformer
data = {'feeder':'IEEE123','capacity':4000}
requests.post(db_address+'transformer',json=data)
#requests.put(db_address+'transformers/1',json=data)
#requests.get(db_address+'transformers').json()

#Set up users

#Address
for user_no in range(1,no_users+1):
	data = {'address':'Main Street '+str(user_no),'city':'Aspen','country':'US','postal_code':'00000'}
	requests.post(db_address+'address',json=data,auth=(user_name,pw))
	#address = requests.get(db_address+'addresses').json()
	#Service location
	data = {'address_id':user_no,'map_location':'somewhere'}
	requests.post(db_address+'service_location',json=data,auth=(user_name,pw))
	#service_locations = requests.get(db_address+'service_locations').json()
	#Home hub
	data = {'service_location_id':user_no,'market_id':1}
	requests.post(db_address+'home_hub',json=data,auth=(user_name,pw))
	#hhs = requests.get(db_address+'home_hubs').json()
	#Meter
	data = {'utility_id':1,'service_location_id':user_no,'home_hub_id':user_no,'feeder':'IEEE123','substation':'HCE-Xcel','meter_type':'Residential'}
	requests.post(db_address+'meter',json=data,auth=(user_name,pw))
	#meters = requests.get(db_address+'meters').json()
	#PV
	data = {'home_hub_id':user_no,'meter_id':user_no,'q_rated':4000,'is_active':True}
	requests.post(db_address+'pv',json=data,auth=(user_name,pw))
	#pvs = requests.get(db_address+'pvs').json()

# Meter interval data only gets written during operations. The following lines are just a reminder for commands to be used with requests.

#Meter interval
#data = {'meter_id':1,'rate_id':1,'start_time':str(pd.Timestamp(2000,1,1,0,0)),'end_time':str(pd.Timestamp(2000,1,1,0,5)),'e':0.0,'qmtp':0.0,'p_bid':0.0,'q_bid':0,'is_bid':True}
#requests.post(db_address+'meter_interval',json=data,auth=(user_name,pw))
#mis = requests.get(db_address+'meter_intervals').json()
#Market interval

#Get multiple bids
#requests.get(db_address+'bids/?is_supply=true&start_time=2019-01-01').json()
#equests.get(db_address+'bids/?is_supply=false&start_time=2019-01-01').json()
