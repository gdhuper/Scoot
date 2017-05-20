# Import the basemap package
from mpl_toolkits.basemap import Basemap
import scoot as sc
import matplotlib.pyplot as plt

startlat, startlon = sc.getLatLong()

print(list(startlat.astype(float)))


# Create a map on which to draw.  We're using a mercator projection, and showing the whole world.
m = Basemap(llcrnrlon=-122.56,llcrnrlat=37.4,urcrnrlon=-122,urcrnrlat=37.99, epsg=4269)
# Draw coastlines, and the edges of the map.

# Convert latitude and longitude to x and y coordinates
x, y = m(list(startlat.astype(float)), list(startlon.astype(float)))
m.plot(x, y, 'o', markersize=5)
plt.plot(x, y, '-', color='yellow', linewidth = 1.75)
m.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 3000, verbose= True)

# Use matplotlib to draw the points onto the map.
m.scatter(x,y,1,marker='o',color='red')
# Show the plot.
plt.figure()
plt.show()