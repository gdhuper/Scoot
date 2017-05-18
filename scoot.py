import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sys
from mpl_toolkits.basemap import Basemap


def readAndFilterData():
	#creating pandas dataframe from csv file
	scoot_rides_test_data = pd.read_csv(sys.argv[1])
	
	
	lat = scoot_rides_test_data['start_lat'].tolist()
	lon = scoot_rides_test_data['start_lon'].tolist()

	drawMap(lat, lon)






def drawMap(lat, lon):
	# Create a map on which to draw.  We're using a mercator projection, and showing the whole world.
	m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')
	# Draw coastlines, and the edges of the map.
	m.drawcoastlines()
	m.drawmapboundary()
	# Convert latitude and longitude to x and y coordinates
	x, y = m(lat, lon)
	# Use matplotlib to draw the points onto the map.
	m.scatter(x,y,1,marker='o',color='red')
	# Show the plot.
	plt.show()




if len(sys.argv) > 1:
	readAndFilterData()
else:
	print("usage: scoot.py <path-to-csv-file>")




















