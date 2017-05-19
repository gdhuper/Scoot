import pandas as pd
import numpy as np
from collections import defaultdict
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime as dt
import sys
from mpl_toolkits.basemap import Basemap


#creating pandas dataframe from csv file
scoot_rides_test_df = pd.read_csv('scoot_rides_test.csv')

def parseDate(date):
	if date == '':
		return None
	else:
		return dt.strptime(date, '%m/%d/%Y %H:%M:%S.%f').date()
		
def parseScootMoved(t):
	if t == 'nan' or t == None:
		return False
	else:
		return True

def parseAndFilterData():
	for record in scoot_rides_test_df['start_time_local']:
		#record['start_time_local'] = parseDate(record['start_time_local'])
		print(record)
		print(parseDate(record))
		#record['end_time_local']  = parseDate(record['end_time_local'])
		#record['scoot_moved'] = parseScootMoved(record['scoot_moved'])
		





if len(sys.argv) == 1:
	parseAndFilterData()
else:
	print("usage: scoot.py")




















