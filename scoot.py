import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime as dt
import sys
from mpl_toolkits.basemap import Basemap


def parseDate(date):
	if date == '':
		return None
	else:
		return dt.strptime(date, '%m/%d/%Y %H:%M:%S.%f').date()
		#1/1/2016  12:29:43 PM


def readAndFilterData():
	#creating pandas dataframe from csv file
	scoot_rides_test_data = pd.read_csv('scoot_rides_test.csv')
	for date in scoot_rides_test_data['start_time_local'][:10]:
		print(parseDate(date))


	for date in scoot_rides_test_data['end_time_local'][:10]:
		print(parseDate(date))
		#print(date)

	for date in scoot_rides_test_data['scoot_moved'][:10]:
		print(date)








if len(sys.argv) == 1:
	readAndFilterData()
else:
	print("usage: scoot.py")




















