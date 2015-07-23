###################################
# Cassandra connecting script	    #	 
# Author: Oshadha			    #
# Date: 2010/03/08		    #
###################################

import pycassa
import threading
from pycassa.connection import NoServerAvailable
from datetime import datetime
import sys

# Options | defaults to connecting to the server at 'localhost:9160'
HOST = 'localhost:9160'
keyspace_name = 'TestAppUserData'

# Create the connection and a column family
def create_con_cf(columnfamily_name):
	try:
		lock = threading.Lock()
		lock.acquire()
		connection = pycassa.connect([HOST])
		cf = pycassa.ColumnFamily(connection, keyspace_name, columnfamily_name)
		return cf
	except NoServerAvailable, ex:
		sys.stderr.write('ERROR: %s\n' % str(ex))
	finally:
   		lock.release()

