###################################  # #
# Random script			    #	/| |\
# Author: Oshadha			    # /| |\
# Date: 2010/03/08		    # /| |\
###################################  # #

import random

# Bronx lt = 40.851666, lg = -73.864346
# Manhattan lt = 40.782552, lt = -73.966656
# Queens lt = 40.749199, lg = -73.794823
# Brooklyn lt = 40.647825, lg = -73.944511
# Staten Island lt = 40.580446, lg = -74.151878
# Emerson hill lt = 40.597132,lg = -74.111366

def generate_lglt(lsize):
	bronx_lon, manhattan_lon, queens_lon, brooklyn_lon, crown_lon = -73.864346, -73.966656, -73.794823, -73.944511, -73.944683
	bronx_lat, manhattan_lat, queens_lat, brooklyn_lat, crown_lat = 40.851666, 40.782552, 40.749199, 40.647825, 40.667028
	staten_lon, emerson_lon, staten_lat, emerson_lat = -74.151878, -74.111366, 40.580446, 40.597132
	hillcrist_lon, hillcrit_lat = -73.796368, 40.720912
	lonlats = []
	for x in xrange(lsize, 0, -1):
		lonlats.append((random.uniform(brooklyn_lon, crown_lon),(random.uniform(brooklyn_lat, crown_lat))))
		lonlats.append((random.uniform(queens_lon, hillcrist_lon),(random.uniform(queens_lat, hillcrit_lat))))		
		lonlats.append((random.uniform(bronx_lon, manhattan_lon),(random.uniform(bronx_lat, manhattan_lat))))
		lonlats.append((random.uniform(staten_lon, emerson_lon),(random.uniform(staten_lat, emerson_lat))))
	random.shuffle(lonlats)
	return lonlats
