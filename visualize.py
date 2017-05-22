import sys
import scoot as sc
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import datetime
import matplotlib.mlab as mlab
import numpy as np
import seaborn as sns
from mpl_toolkits.basemap import Basemap
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
from datetime import datetime as dt
import plotly.plotly as py
import plotly
from plotly.graph_objs import *
from pylab import rcParams
rcParams['figure.figsize'] = 13, 7

#replace plotly usename and api_key to draw a graph (will not work since this is my username; need to be logged in as user specified in credentials)
plotly.tools.set_credentials_file(username='gopdhuper', api_key='5jMdPpyquzqza3WeSLO9')





# draws histogram for average ride count for each weekday
def drawWeekDayHist():
    df = sc.getRideCountByDay("w")
    #storing values in a numpy array
    xVals = df.values.ravel()

    dic = {}
    for key, val in zip(xVals, df.index.get_values()):
        dic[val] = key


    objects = ('Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat')
    y_pos = np.arange(len(objects))
    performance = [dic['Sunday'], dic['Monday'], dic["Tuesday"], dic["Wednesday"], dic["Thursday"],dic["Friday"],dic["Saturday"]]
     
    plt.bar(y_pos, performance, align='center', alpha=0.9)
    plt.xticks(y_pos, objects, rotation='vertical')
    plt.ylabel('Ride Count')
    plt.subplots_adjust(bottom=0.15)
    plt.title('Ride Count by weekday')
    plt.show()



# draws histogram for average ride count for each hour in a day
def drawRidePerHourHist():
    df = sc.getRideCountByDay("h")

    dic = {}
    objects = df.index.ravel()
    vals = df.values.ravel()


    #parsing hours and values into a dictionary
    for i, j in zip(objects, vals):
    	i = str(i).split("T")[1].split(":")
    	hour = i[0]
    	dic[hour] = j

    performance = [dic[x] for x in dic]
    
    y_pos = [int(x) for x in dic]
    x_labels = [(x+":00") for x in dic]

    plt.bar(y_pos, performance, align='center', alpha=0.9, color='#CE6F3B')
    plt.xticks(y_pos, x_labels, rotation='vertical')
    plt.ylabel('Ride Count --->')
    plt.xlabel("Hours ---> ")
    plt.subplots_adjust(bottom=0.15)
    plt.title('Avg. Ride Count Per Hour')
    plt.show()

    
   

# draws line graph for rides per day from Jan, 2016 - May, 2017
def drawRideByDay():
	df = sc.getRideCountByDay("d")
	

	years = mdates.YearLocator()   
	months = mdates.MonthLocator() 
	monthsFmt = mdates.DateFormatter('%Y-%m')

	fig, ax = plt.subplots()

	ax.plot(df.index, df.values, color="red")
	fig.subplots_adjust(bottom=0.2)



	ax.xaxis.set_major_locator(months)
	ax.xaxis.set_major_formatter(monthsFmt)
	ax.xaxis.set_minor_locator(years)
	#customizing graph frame 
	rcParams['xtick.major.pad']='8'	

	datemin = df.index.min() #starting date
	
	datemax = df.index.max() #ending date

	ax.set_xlim(datemin, datemax)
	ax.set_xlabel("Months (January 1, 2016 - May 12, 2017)")
	ax.set_ylabel("Rides")

	fig.autofmt_xdate()
	plt.show()


def drawHotSpotsForTopUsers():
	#lat, lon = sc.getLatLong()
	top_start_lat, top_start_lon, top_end_lat, top_end_lon, low_start_lat, low_start_lon, low_end_lat, low_end_lon = sc.getLocsOfUserRideCount()
		
	mapbox_access_token = 'pk.eyJ1IjoiZ29wZGh1cGVyIiwiYSI6ImNqMnpkbmg4ZzAwNzIzM3FpNWV0OGQ0YXYifQ.NEcJOsCugDOQJz-sGdq2sg'

	data_start_top = Scattermapbox(lat=top_start_lat.tolist(),
			lon=top_start_lon.tolist(),
	        mode='markers',
	        marker=Marker(
	            size=3,
	            color="blue"
	        ),
	        text=['Top Starting Point'],
	        
	    )
	data_end_top =  Scattermapbox(lat=top_end_lat.tolist(),
        	lon=top_end_lon.tolist(),
	        mode='markers',
	        marker=Marker(
	            size=3,
	            color="red"
	        ),
	       	text=['Top Ending Point'],

	    )
	data_start_low = Scattermapbox(lat=low_start_lat.tolist(),
			lon=low_start_lon.tolist(),
	        mode='markers',
	        marker=Marker(
	            size=3,
	            color="cyan"
	        ),
	        text=['Lowest Starting Point'],
	        
	    )
	data_end_low =  Scattermapbox(lat=low_end_lat.tolist(),
        	lon=low_end_lon.tolist(),
	        mode='markers',
	        marker=Marker(
	            size=3,
	            color="magenta"
	        ),
	       	text=['Lowest Ending Point'],

	    )
	data = Data([data_start_top, data_end_top, data_start_low, data_end_low])

	layout = Layout(
	    autosize=True,
	    hovermode='closest',
	    mapbox=dict(
	        accesstoken=mapbox_access_token,
	        bearing=0,
	        center=dict(
	            lat=37.760139,
	            lon=-122.443373
	        ),
	        pitch=0,
	        zoom=10
	    ),
	   
	)

	fig = dict(data=data, layout=layout)
	py.plot(fig, filename='Multiple Mapbox')



# draws hist for ride count by vehicle type 
def drawRideCountByVehicleType():
	df = sc.getCountByVehicleType()
	print(df.index)

	xVals = df.values.ravel()
	dic = {}
	for key, val in zip(xVals, df.index.get_values()):
		dic[val] = key

	objects = ('1', '3', '4', '5', '6', '7')
	y_pos = np.arange(len(objects))
	performance = [dic[1], dic[3], dic[4], dic[5], dic[6],dic[7]]
	plt.bar(y_pos, performance, align='center', alpha=0.9)
	plt.xticks(y_pos, objects, rotation='vertical')
	plt.ylabel('Ride Count --->')
	plt.xlabel('<-- Vehicle ID --->')
	plt.subplots_adjust(bottom=0.15)

	plt.title('Ride count by Vehicle type')
	plt.show()

# draws hist for ride count by vehicle type 
def drawMileageByVehicleType():
	df = sc.getTotalMileageByVehicleType()
	print(df.index)

	xVals = df.values.ravel()
	dic = {}
	for key, val in zip(xVals, df.index.get_values()):
		dic[val] = key

	objects = ('1', '3', '4', '5', '6', '7')
	y_pos = np.arange(len(objects))
	performance = [dic[1], dic[3], dic[4], dic[5], dic[6],dic[7]]
	plt.bar(y_pos, performance, align='center', alpha=0.9)
	plt.xticks(y_pos, objects, rotation='vertical')
	plt.ylabel('Mileage --->')
	plt.xlabel('<-- Vehicle ID --->')
	plt.subplots_adjust(bottom=0.15)

	plt.title('Total Mileage by Vehicle type')
	plt.show()

# draws hist for ride count by vehicle type 
def drawMileageDistribution():
	df = sc.getRideMileageDistribution()

	xvals = []
	yvals = []
	for k in df:
		xvals.append(k)
		yvals.append(df[k])
	

	fig, ax = plt.subplots()

	ax.plot(xvals, yvals, color="red")
	fig.subplots_adjust(bottom=0.2)


	rcParams['xtick.major.pad']='8'	

	datemin = 0 #starting mile range
	
	datemax = 9 #ending mile range

	ax.set_xlim(datemin, datemax)
	ax.set_xlabel("<-- Miles -->")
	ax.set_ylabel("Ride Count -->")
	ax.set_title("Distribution of Ride Mileage")

	fig.autofmt_xdate()
	plt.xticks(rotation='horizontal')

	plt.show()


    
# Draws hot spots on map using plotly. (will only work with a valid access token)
def drawHotSpots():
	start_lat, start_lon, end_lat, end_lon = sc.latLongForTopLocs(5)
		
	mapbox_access_token = 'pk.eyJ1IjoiZ29wZGh1cGVyIiwiYSI6ImNqMnkxcHVtdzAxNDIycW1rNDNieHM0N2MifQ.qI0GSdz260V22vUG2CfjGw'

	data_start = Scattermapbox(lat=start_lat.tolist(),
			lon=start_lon.tolist(),
	        mode='markers',
	        marker=Marker(
	            size=3,
	            color="blue"
	        ),
	        text=['Starting Point'],
	        
	    )
	data_end =  Scattermapbox(lat=end_lat.tolist(),
        	lon=end_lon.tolist(),
	        mode='markers',
	        marker=Marker(
	            size=3,
	            color="red"
	        ),
	       	text=['Ending Point'],

	    )
	data = Data([data_start, data_end])

	layout = Layout(
	    autosize=True,
	    hovermode='closest',
	    mapbox=dict(
	        accesstoken=mapbox_access_token,
	        bearing=0,
	        center=dict(
	            lat=37.760139,
	            lon=-122.443373
	        ),
	        pitch=0,
	        zoom=10
	    ),
	   
	)

	fig = dict(data=data, layout=layout)
	py.plot(fig, filename='Multiple Mapbox')




# drawWeekDayHist()
drawRidePerHourHist()
# drawRideByDay()
# drawHotSpotsForTopUsers()
# drawHotSpots()
# drawMileageDistribution()
# drawRidePerHourHist()
# drawRideCountByVehicleType()
# drawCountByUser()
