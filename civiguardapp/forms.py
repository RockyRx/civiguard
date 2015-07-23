from django.forms import ModelForm
from django import forms
from django.forms.widgets import RadioSelect
from testproject.testapplication.models import CiviguardUsersModel, CiviguardUpdates
from django.http import HttpResponseRedirect


PHONETYPE_CHOICES = (
    ('iPhone', 'iPhone'),
    ('Android', 'Android'),
    ('BlackBerry', 'BlackBerry'),
)


class CiviguardUsers(forms.Form):
    	fullName 		= forms.CharField(max_length=20)
	emailAdd		= forms.EmailField()
	password2 		= forms.CharField(max_length=10)
	cellPhone 		= forms.CharField(max_length=30)
	phoneType 		= forms.ChoiceField(widget=RadioSelect(), choices=PHONETYPE_CHOICES)


class CiviguardUsersLogin(forms.Form):
	emailAdd		= forms.EmailField()
	password		= forms.CharField(max_length=10)


class CiviguardUsersForm(ModelForm):
    class Meta:
        model = CiviguardUsersModel


class CiviguardUpdatesForm(ModelForm):
	class Meta:
		model = CiviguardUpdates



