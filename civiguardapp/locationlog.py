###################################
# Random user script		    #	 
# Author: Oshadha			    #
# Date: 2010/03/08		    #
###################################

from testproject.testapplication.models import CiviguardUsersModel, LocationLogger
from django.utils import simplejson
from googlemaps import GoogleMaps, GoogleMapsError
import random
import sys

def func_user(user_data):
	try:
		u_data = list(simplejson.loads(user_data))
		userid = u_data[0]
		del u_data[0]
		users = CiviguardUsersModel.objects.get(userKey=userid)
		u_email = users.emailAdd
		x_locale = ''
		y_locale = ''
		for i in range(len(u_data)):
			if u_data[i][2] == "lacale":
				x_locale += str(u_data[i][0]) + ',' + str(u_data[i][1]) + ','
			if u_data[i][2] == "poi":
				y_locale += str(u_data[i][0]) + ',' + str(u_data[i][1]) + ','
		location = LocationLogger()
		location.email = u_email
		location.x_locale = x_locale
		location.y_locale = y_locale
		location.status = 'saved'
		location.save()
		return y_locale
	except TypeError, ex:
		#sys.stderr.write('Type error %s' % str(ex))
		return str(ex)


def get_locale(u_email):		
	try:
		userlst = LocationLogger.objects.get(email=u_email)
		locale = list(userlst.x_locale.split(','))
		locale.remove("")
		poi = list(userlst.y_locale.split(',')) 
		poi.remove("")
		dict = {}
		dict["data"] = []
		x_1 = 0
		y_1 = 1
		x_2 = 0
		y_2 = 1
		for i in xrange(len(locale)):
			try:
				dict['data'].append({'type': 'locale', 'lat': locale[i + x_1], 'lon': locale[i + y_1]})
				x_1 += 1
				y_1 += 1
			except Exception, ex:
				pass
		for i in xrange(len(poi)):
			try:
				dict['data'].append({'type': 'poi', 'lat': poi[i + x_2], 'lon': poi[i + y_2]})
				x_2 += 1
				y_2 += 1			
			except Exception, ex:
				pass
		jsonobj = simplejson.dumps(dict)
		return jsonobj
	except TypeError, ex:
		sys.stderr.write('Type error %s' % str(ex))

		
					