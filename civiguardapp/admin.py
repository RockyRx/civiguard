from django.contrib import admin
from testproject.testapplication.models import CiviguardUsersModel, CiviguardUpdates, LocationLogger

admin.site.register(CiviguardUsersModel)
admin.site.register(CiviguardUpdates)
admin.site.register(LocationLogger)