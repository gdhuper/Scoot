"""
Example of animation
"""
from geoplotlib.layers import BaseLayer
from geoplotlib.core import BatchPainter
import geoplotlib
from geoplotlib.colors import colorbrewer
from geoplotlib.utils import epoch_to_str, BoundingBox, read_csv


class TrailsLayer(BaseLayer):

    def __init__(self):
        self.data = read_csv('taxi.csv')
        #self.data1 = read_csv('taxi.csv')
        self.cmap = colorbrewer(self.data['taxi_id'], alpha=220)
        self.t = self.data['timestamp'].min()
        self.painter = BatchPainter()


    def draw(self, proj, mouse_x, mouse_y, ui_manager):
        self.painter = BatchPainter()
        df = self.data.where((self.data['timestamp'] > self.t) & (self.data['timestamp'] <= self.t + 15*60))

        for taxi_id in set(df['taxi_id']):
            grp = df.where(df['taxi_id'] == taxi_id)
            self.painter.set_color(self.cmap[taxi_id])
            x, y = proj.lonlat_to_screen(grp['lon'], grp['lat'])
            self.painter.points(x, y, 10)

        self.t += 2*60

        if self.t > self.data['timestamp'].max():
            self.t = self.data['timestamp'].min()

        self.painter.batch_draw()
        ui_manager.info(epoch_to_str(self.t))


    def bbox(self):
        return BoundingBox(north=40.110222, west=115.924463, south=39.705711, east=116.803369)


geoplotlib.add_layer(TrailsLayer())
geoplotlib.show()





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