import pandas as pd
import numpy as np
from collections import defaultdict
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime as dt
from dateutil import rrule
import sys
from mpl_toolkits.basemap import Basemap
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import calendar as cal



#creating  dataframe from csv file
scoot_rides_test_df = pd.read_csv('scoot_rides_test.csv')

#another dataframe to store records whenre scoot_moved = True
scoot_rides_if_moved_df = scoot_rides_test_df[scoot_rides_test_df['scoot_moved'] == 't']
pd.options.mode.chained_assignment = None

#parse date from string object
def parseDate(datetime, groupBy):
	if datetime == '':
		return None
	else:
		if groupBy == "d":
			return dt.strptime(datetime.split(" ")[0], '%m/%d/%Y').date()
		elif groupBy == "h":
			time = datetime.split(" ")[1]
			HM = time.split(":")[0]
			return dt.strptime(HM, '%H')
		elif groupBy == 'w':
			date = dt.strptime(datetime.split(" ")[0], '%m/%d/%Y').date()
			return cal.day_name[date.weekday()]
		else:
			print("Select valid entity: <h - hours, d - day, w - weekday>")


#Helper method to get miles from odometer reading
def getMiles(start_odometer, end_odometer):
	return abs(end_odometer - start_odometer)


#Helper method to standardize rides on a day in a week
def standardizeWeekCount(value):
	startDate = parseDate(scoot_rides_test_df['start_time_local'].iloc[0], "d")
	endDate = parseDate(scoot_rides_test_df['start_time_local'].iloc[-1], "d")
	total_weeks = rrule.rrule(rrule.WEEKLY, dtstart=startDate, until=endDate)
	return int(value / total_weeks.count())

def standardizeRidesPerHour(rides):
	return int(rides / 24)


#Gets ride count for each day if scoot_moved == True
# Returns Ride count for each day
# param: groupby (optional), to get rides per hour
def getRideCountByDay(groupBy):
	scoot_rides_if_moved_df.loc[: ,"start_date"]= scoot_rides_if_moved_df['start_time_local'].apply(lambda d: parseDate(d, groupBy))
	if groupBy == "d":
		return pd.value_counts(scoot_rides_if_moved_df['start_date'].values).sort_index()
	elif groupBy == "h":
		#return pd.value_counts(scoot_rides_if_moved_df['start_date'].values).sort_index()
		temp = pd.value_counts(scoot_rides_if_moved_df['start_date'].values).sort_index()
		temp = temp.to_frame()
		temp.loc[:, 0] = temp[0].apply(lambda x: standardizeRidesPerHour(x))
		return temp
	elif groupBy == "w":
		temp = pd.value_counts(scoot_rides_if_moved_df['start_date'].values).sort_index()
		temp = temp.to_frame()
		temp.loc[:, 0] = temp[0].apply(lambda x: standardizeWeekCount(x))
		return temp

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


	



if len(sys.argv) > 1:
	rides_per_day = getRideCountByDay(sys.argv[1])
	print(rides_per_day)
	#print(rides_per_day)
	#geRideCountByUser()
	#getCountByVehicleType()
	#getTotalMileageByVehicleType()
	#getRideMileageDistribution()
	#getTopLocsByVolume(4)
else:
	print("usage: scoot.py <group-by>")




















