import pycassa
from testproject.testapplication.db_connection import create_con_cf

class CassandraMap():
	f_name       	    = pycassa.String()
	l_name	          = pycassa.String()
	geo_location	    = pycassa.String()
	zip_code 		    = pycassa.Int64()
	cell_phone 		    = pycassa.Int64()
#	cell_service_pro	    = pycassa.String()
#	cell_type		    = pycassa.String()
	facebook_id 	    = pycassa.String()
	twitter_id 		    = pycassa.String()
	password 		    = pycassa.String()


class LocationLogger():
	longitude = pycassa.Float64()
	latitude = pycassa.Float64()
	l_name = pycassa.String()
	f_name = pycassa.String()
	status = pycassa.String()


def processing_data(classval):
	try:
		if isinstance(classval, CassandraMap):
			cf = create_con_cf('UserData')
			CassandraMap.objects = pycassa.ColumnFamilyMap(CassandraMap, cf)
			return CassandraMap()
		else:
			cf = create_con_cf('LocationLogger')
			LocationLogger.objects = pycassa.ColumnFamilyMap(LocationLogger, cf)
			return LocationLogger()	
	except TypeError, ex:
		print "Type Error"
