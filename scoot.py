import pandas as pd
import numpy as np
from collections import defaultdict
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime as dt
import sys
from mpl_toolkits.basemap import Basemap
import matplotlib.dates as mdates
import matplotlib.cbook as cbook



#creating  dataframe from csv file
scoot_rides_test_df = pd.read_csv('scoot_rides_test.csv')

#another dataframe to store records whenre scoot_moved = True
scoot_rides_if_moved_df = scoot_rides_test_df[scoot_rides_test_df['scoot_moved'] == 't']

#parse date from string object
def parseDate(datetime):
	if datetime == '':
		return None
	else:
		print(datetime.split(" ")[0] + " : " +  datetime.split(" ")[1] )
		#return dt.strptime(date, '%m/%d/%Y').date()


#Helper method to get miles from odometer reading
def getMiles(start_odometer, end_odometer):
	return abs(end_odometer - start_odometer)



#Gets ride count for each day if scoot_moved == True
def getRideCountByDay():
	scoot_rides_by_day_df = scoot_rides_test_df[scoot_rides_test_df['scoot_moved'] == 't']
	scoot_rides_by_day_df['start_date'] = scoot_rides_if_moved_df['start_time_local'].apply(lambda d: parseDate(d))
	print(pd.value_counts(scoot_rides_by_day_df['start_date'].values).sort_index())
	return pd.value_counts(scoot_rides_by_day_df['start_date'].values).sort_index()



def geRideCountByUser():
	scoot_rides_by_user_df = scoot_rides_test_df[scoot_rides_test_df['scoot_moved'] == 't']
	scoot_rides_test_df['user_count'] = pd.value_counts(scoot_rides_test_df['user_id'].values)
	print(pd.value_counts(scoot_rides_test_df['user_id'].values))
	return pd.value_counts(scoot_rides_test_df['user_id'].values)


def getCountByVehicleType():
	scoot_rides_by_user_df = scoot_rides_test_df[scoot_rides_test_df['scoot_moved'] == 't']
	scoot_rides_test_df['count_by_vehicle_type'] = pd.value_counts(scoot_rides_test_df['vehicle_type_id'].values)
	print(pd.value_counts(scoot_rides_test_df['vehicle_type_id'].values))
	return pd.value_counts(scoot_rides_test_df['vehicle_type_id'].values)


def getTotalMileageByVehicleType():
	scoot_rides_by_user_df = scoot_rides_test_df[scoot_rides_test_df['scoot_moved'] == 't']
	scoot_rides_by_user_df =scoot_rides_by_user_df.dropna(axis=0, how='any')
	scoot_rides_by_user_df['mileage'] = scoot_rides_by_user_df.apply(lambda row: getMiles(row['start_odometer'], row['end_odometer']), axis=1)
	print(scoot_rides_by_user_df.groupby(by=['vehicle_type_id'])['mileage'].sum())
	

def getRideMileageDistribution():
	scoot_rides_by_user_df = scoot_rides_test_df[scoot_rides_test_df['scoot_moved'] == 't']
	scoot_rides_by_user_df =scoot_rides_by_user_df.dropna(axis=0, how='any')
	scoot_rides_by_user_df['mileage'] = scoot_rides_by_user_df.apply(lambda row: getMiles(row['start_odometer'], row['end_odometer']), axis=1)
	print(scoot_rides_by_user_df['mileage'])


def getTopLocsByVolume(numberOfLocs):
	scoot_rides_by_location_df = scoot_rides_test_df[scoot_rides_test_df['scoot_moved'] == 't']
	scoot_rides_by_location_df =scoot_rides_by_location_df.dropna(axis=0, how='any')
	print(pd.value_counts(scoot_rides_by_location_df['start_location_id']).head(5))
	print(pd.value_counts(scoot_rides_by_location_df['end_location_id']).head(5))

def getLocsByTime(hour):
	scoot_rides_test_df = scoot_rides_test_df[scoot_rides_test_df['scoot_moved'] == 't']
	scoot_rides_test_df =scoot_rides_test_df.dropna(axis=0, how='any')


	



if len(sys.argv) == 1:
	getRideCountByDay()
	#geRideCountByUser()
	#getCountByVehicleType()
	#getTotalMileageByVehicleType()
	#getRideMileageDistribution()
	#getTopLocsByVolume(4)
else:
	print("usage: scoot.py")




















