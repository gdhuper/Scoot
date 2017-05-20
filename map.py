# """
# Example of animation
# """
# from geoplotlib.layers import BaseLayer
# from geoplotlib.core import BatchPainter
# import geoplotlib
# from geoplotlib.colors import colorbrewer
# from geoplotlib.utils import epoch_to_str, BoundingBox, read_csv


# class TrailsLayer(BaseLayer):

#     def __init__(self):
#         self.data = read_csv('taxi.csv')
#         #self.data1 = read_csv('taxi.csv')
#         self.cmap = colorbrewer(self.data['taxi_id'], alpha=220)
#         self.t = self.data['timestamp'].min()
#         self.painter = BatchPainter()


#     def draw(self, proj, mouse_x, mouse_y, ui_manager):
#         self.painter = BatchPainter()
#         df = self.data.where((self.data['timestamp'] > self.t) & (self.data['timestamp'] <= self.t + 15*60))

#         for taxi_id in set(df['taxi_id']):
#             grp = df.where(df['taxi_id'] == taxi_id)
#             self.painter.set_color(self.cmap[taxi_id])
#             x, y = proj.lonlat_to_screen(grp['lon'], grp['lat'])
#             self.painter.points(x, y, 10)

#         self.t += 2*60

#         if self.t > self.data['timestamp'].max():
#             self.t = self.data['timestamp'].min()

#         self.painter.batch_draw()
#         ui_manager.info(epoch_to_str(self.t))


#     def bbox(self):
#         return BoundingBox(north=40.110222, west=115.924463, south=39.705711, east=116.803369)


# geoplotlib.add_layer(TrailsLayer())
# geoplotlib.show()





'''
def drawMap(scoot_rides_test_data):
	# Create a map on which to draw.  We're using a mercator projection, and showing the whole world.
	m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')
	# Draw coastlines, and the edges of the map.
	m.drawcoastlines()
	m.drawmapboundary()
	# Convert latitude and longitude to x and y coordinates
	x, y = m(list(scoot_rides_test_data["start_lat"].astype(float)), list(scoot_rides_test_data["start_lon"].astype(float)))
	# Use matplotlib to draw the points onto the map.
	m.scatter(x,y,1,marker='o',color='red')
	# Show the plot.
	plt.show()
'''



# 


import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import scoot as sc
import sys
#np.random.seed(0)



df = sc.getRideCountByDay(sys.argv[1])
xVals = df.values.ravel()
# example data
mu = xVals.mean()  # mean of distribution
sigma = xVals.std()  # standard deviation of distribution
x = xVals
print(x)
num_bins = 7

fig, ax = plt.subplots()

# the histogram of the data
n, bins, patches = ax.hist(x, num_bins, normed=1)
print(n, bins, patches)

# add a 'best fit' line
y = mlab.normpdf(bins, mu, sigma)
ax.plot(bins, y, '--')
ax.set_xlabel('Days of week')
ax.set_ylabel('Ride Count')
ax.set_title(r'Histogram of IQ: $\mu=100$, $\sigma=15$')

# Tweak spacing to prevent clipping of ylabel
fig.tight_layout()
plt.show()







# """
# Make a histogram of normally distributed random numbers and plot the
# analytic PDF over it
# """

# import sys
# import scoot as sc
# import matplotlib.pyplot as plt; plt.rcdefaults()
# import numpy as np
# import matplotlib.pyplot as plt


# df = sc.getRideCountByDay(sys.argv[1])
# xVals = df.values.ravel()

# dic = {}
# for key, val in zip(xVals, df.index.get_values()):
# dic[val] = key
# print(dic)

# #print(df.index.get_values())
# objects = ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')
# y_pos = np.arange(len(objects))
# performance = [dic['Sunday'], dic['Monday'], dic["Tuesday"], dic["Wednesday"], dic["Thursday"],dic["Friday"],dic["Saturday"]]
 
# plt.bar(y_pos, performance, align='center', alpha=0.7)
# plt.xticks(y_pos, objects)
# plt.ylabel('User Count')
# plt.title('Daily User Count')
 


# plt.show()
