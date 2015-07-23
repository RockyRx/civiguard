from django.db import models
from django import forms
from django.forms.widgets import HiddenInput
from django.forms import ModelForm
	

class CiviguardUsersModel(models.Model):
	fullName 		= models.CharField(max_length=100)
	emailAdd		= models.EmailField(primary_key=True)
	password2 		= models.CharField(max_length=100)
	cellPhone 		= models.CharField(max_length=30)
	phoneType 		= models.CharField(max_length=10)
	activated		= models.BooleanField(default=0)
	userKey		= models.CharField(max_length=255, blank=True)
	mobVerCode		= models.IntegerField(max_length=15, blank=True)
	passResetCode		= models.CharField(max_length=255, blank=True)
	region			= models.CharField(max_length=100, blank=True)
	
	def __unicode__(self):
		return u'%s %s %s' % (self.fullName, self.emailAdd, self.password2)


class CiviguardUpdates(models.Model):
	name 			= models.CharField(max_length=100)
	ipAddress		= models.CharField(max_length=50)

	def __unicode__(self):
		return u'%s %s %s' % (self.name, self.ipAddress)


class LocationLogger(models.Model):
	email	 			= models.CharField(primary_key=True, max_length=100)
	x_locale 	 		= models.CharField(max_length=250)
	y_locale 			= models.CharField(max_length=250)
	status 			= models.CharField(max_length=20)

	def __unicode__(self):
		return u'%s %s' % (self.email, self.status)
	

class AliasLocation(models.Model):
	userName 			= models.CharField(max_length=20)
	alias_name			= models.CharField(max_length=20)
	alias_longitude 		= models.FloatField(max_length=20)
	alias_longitude 		= models.FloatField(max_length=20)


