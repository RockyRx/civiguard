from django.conf.urls.defaults import *
from testapplication import views
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',('^$', views.test_form),
				  (r'^check-form/$', views.check_form),
				  (r'^save-form/$', views.save_form),	
				  (r'^thanks/$', views.thanks),
				  (r'^getupdates/$', views.getupdates),
				  (r'^updates/$', views.save_updates),
				  (r'^signup/$', views.signup),
				  (r'^confirmation/$', views.confirmation),
				  (r'^login/$', views.login_page),
				  (r'^login_save/$', views.user_login),
                              (r'^verification/$', views.mobile_ver),
				  (r'^complete/$', views.complete),
				  (r'^email/$', views.email),
				  (r'^fgpass/$', views.fgpass),
				  (r'^resetmail/$', views.resetmail),
				  (r'^resetpage/$', views.resetpage),
				  (r'^resetpassword/$', views.resetpassword),
				  (r'^userinfo/$', views.edituser),
				  (r'^localeset/$', views.localeset),
				  (r'^getlocale/$', views.getlocale),
				  (r'^load_map/$', views.load_map),
				  (r'^logout/$', views.logout),
				  (r'^test/$', views.test), 				  
				  (r'^fb/$', views.facebook),				  
				  (r'^activate/(?P<key>\w+)/$', views.activate_account),				
				  (r'^validate/$', views.validate_user),


    # Example:
    # (r'^civiguard/', include('civiguard.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^civiguard/admin/', include(admin.site.urls)),
)