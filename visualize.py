import sys
import scoot as sc
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import datetime
import numpy as np

import matplotlib.dates as mdates
import matplotlib.cbook as cbook
from datetime import datetime as dt
from pylab import rcParams
rcParams['figure.figsize'] = 13, 7




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
	datafile = cbook.get_sample_data('goog.npy')
	

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


def drawCountByUser():
	user_count = sc.geRideCountByUser()
	print(user_count)



drawRidePerHourHist()

#drawCountByUser()


#drawRideByDay()


# drawWeekDayHist()
