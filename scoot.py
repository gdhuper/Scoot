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
scoot_rides_if_moved_df =scoot_rides_if_moved_df.dropna(axis=0, how='any')


#parse date from string object
def parseDate(datetime, groupBy):
	if datetime == '':
		return None
	else:
		if groupBy == "d":
			#print(dt.strptime(datetime.split(" ")[0], '%m/%d/%Y').date())
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


#Helper function to get miles from odometer reading
def getMiles(start_odometer, end_odometer):
	return abs(end_odometer - start_odometer)


#Helper function to standardize rides on a day in a week
def standardizeWeekCount(value):
	startDate = parseDate(scoot_rides_test_df['start_time_local'].iloc[0], "d")
	endDate = parseDate(scoot_rides_test_df['start_time_local'].iloc[-1], "d")
	total_weeks = rrule.rrule(rrule.WEEKLY, dtstart=startDate, until=endDate)
	return int(value / total_weeks.count())

# Helper function to standardize rides per hour
def standardizeRidesPerHour(rides):
	return int(rides / 24)


# Gets ride count for each day if scoot_moved == True
# Returns Ride count for each day
# param: groupby (optional), to get rides per hour
def getRideCountByDay(groupBy):
	scoot_rides_if_moved_df["start_date"]= scoot_rides_if_moved_df['start_time_local'].apply(lambda d: parseDate(d, groupBy))
	if groupBy == "d":
		return pd.value_counts(scoot_rides_if_moved_df['start_date'].values).sort_index()

	elif groupBy == "h":
		temp = pd.value_counts(scoot_rides_if_moved_df['start_date'].values).sort_index()
		temp = temp.to_frame()
		temp.loc[:, 0] = temp[0].apply(lambda x: standardizeRidesPerHour(x))
		return temp

	elif groupBy == "w":
		temp = pd.value_counts(scoot_rides_if_moved_df['start_date'].values).sort_index()
		temp = temp.to_frame()
		temp.loc[:, 0] = temp[0].apply(lambda x: standardizeWeekCount(x))
		return temp



# Gets ride count by user
def geRideCountByUser():
	scoot_rides_if_moved_df['user_count'] = pd.value_counts(scoot_rides_if_moved_df['user_id'].values)
	return pd.value_counts(scoot_rides_if_moved_df['user_id'].values)

# gets top locations for users with most ride counts
def getLocsOfUserRideCount():
	user_ride_count = geRideCountByUser()
	top_20_users = user_ride_count.head(5)
	lowest_20_users = user_ride_count.tail(20)

	top_start_loc_latLon = scoot_rides_if_moved_df[scoot_rides_test_df['user_id'].isin(top_20_users.index)]
	top_end_loc_latLon = scoot_rides_if_moved_df[scoot_rides_test_df['user_id'].isin(top_20_users.index)]

	lowest_start_loc_latLon = scoot_rides_if_moved_df[scoot_rides_test_df['user_id'].isin(lowest_20_users.index)]
	lowest_end_loc_latLon = scoot_rides_if_moved_df[scoot_rides_test_df['user_id'].isin(lowest_20_users.index)]

	top_start_lat, top_start_lon, top_end_lat, top_end_lon = top_start_loc_latLon['start_lat'], top_start_loc_latLon['start_lon'], top_end_loc_latLon['end_lat'], top_end_loc_latLon['end_lon']
	low_start_lat, low_start_lon, low_end_lat, low_end_lon = lowest_start_loc_latLon['start_lat'], lowest_start_loc_latLon['start_lon'], lowest_end_loc_latLon['end_lat'], lowest_end_loc_latLon['end_lon']

	return top_start_lat, top_start_lon, top_end_lat, top_end_lon, low_start_lat, low_start_lon, low_end_lat, low_end_lon


# gets ride count by vehicle type
def getCountByVehicleType():
	scoot_rides_if_moved_df['count_by_vehicle_type'] = pd.value_counts(scoot_rides_if_moved_df['vehicle_type_id'].values)
	return pd.value_counts(scoot_rides_test_df['vehicle_type_id'].values)


# gets total mileage by vehicle type
def getTotalMileageByVehicleType():
	scoot_rides_if_moved_df['mileage'] = scoot_rides_if_moved_df.apply(lambda row: getMiles(row['start_odometer'], row['end_odometer']), axis=1)
	return scoot_rides_if_moved_df.groupby(by=['vehicle_type_id'])['mileage'].sum()
	
# gets number of rides for each mile distribution
def getRideMileageDistribution():
	scoot_rides_if_moved_df['mileage'] = scoot_rides_if_moved_df.apply(lambda row: getMiles(row['start_odometer'], row['end_odometer']), axis=1)
	dic = {}
	for i in range(0, 10):
		dic[i] = len(scoot_rides_if_moved_df[(scoot_rides_if_moved_df['mileage'] >= i) &  (scoot_rides_if_moved_df['mileage'] <= i+1)]['mileage'])
	return dic

# gets top locations coordinates
def getTopLocsByVolume(numberOfLocs):
	top_start_loc = pd.value_counts(scoot_rides_if_moved_df['start_location_id']).head(numberOfLocs)
	top_end_loc = pd.value_counts(scoot_rides_if_moved_df['end_location_id']).head(numberOfLocs)
	return top_start_loc, top_end_loc


# get start and end coordinates (lat and lon ) for top locations
def latLongForTopLocs(numlocs):
	top_start_loc, top_end_loc = getTopLocsByVolume(numlocs)
	# get coordinated for top locations
	top_start_loc_latLon = scoot_rides_if_moved_df[scoot_rides_test_df['start_location_id'].isin(top_start_loc.index)]
	top_end_loc_latLon = scoot_rides_if_moved_df[scoot_rides_test_df['end_location_id'].isin(top_end_loc.index)]

	return top_start_loc_latLon['start_lat'], top_start_loc_latLon['start_lon'], top_end_loc_latLon['end_lat'], top_end_loc_latLon['end_lon']



count = getRideCountByDay("w")
print(count)

	


# s = getCountByVehicleType()
# print("Id.  Ride Count")
# print(s)

# loc, loc2 = getTopLocsByVolume(5)
# print("Top 5 starting locations:")
# print("Loc.ID   Count")
# print(loc)
# print("Top 5 ending locations:")
# print("Loc.ID   Count")
# print(loc2)
# ride = getRideMileageDistribution()
# print(ride)

#getLocsOfUserRideCount()
# temp = getRideMileageDistribution()
# print(temp)


# rides_per_day = getRideCountByDay(sys.argv[1])
# dic = {} 
# indices = rides_per_day.index
# vals = rides_per_day.values.ravel()
# for key, val in zip(indices, vals):
# 	tempkey = str(key).split(" ")[1]
# 	time = tempkey.split(":")[0] + ":" + tempkey.split(":")[1]
# 	dic[time] = val


# print('Hour:            ', end="")
# for k in dic:
# 	print(k, end='|')
# print("")
# print("Avg. Ride Count: ", end="")
# for k in dic:
# 	print('{:>5}'.format(dic[k]), end='')
	
# if len(sys.argv) > 0:
# 	#latLongForTopLocs(5)

# 	# start, end = getTopLocsByVolume(5)
# 	# print(start.index, end)


# 	#print(rides_per_day)
# 	#geRideCountByUser()
	#getCountByVehicleType()
	#print(getCountByVehicleType())
	#getTotalMileageByVehicleType()
	#getRideMileageDistribution()
	# s, e = getTopLocsByVolume(5)
	# print(s)
	#geRideCountByUser()
	#getCountByVehicleType()
	#getTotalMileageByVehicleType()
	#getRideMileageDistribution()
	#getTopLocsByVolume(4)
# else:
# 	print("usage: scoot.py <group-by>")




















