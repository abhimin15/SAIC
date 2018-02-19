from django.conf.urls import patterns,url,include
import views

urlpatterns = [

    # Main web portal entrance.
    url(r'^$', views.portal_main_page),
    url(r'^verify/(?P<hash>\w+)',views.verify_page),
    url(r'^verify_alumni/(?P<hash>\w+)',views.verify_alumni),
    url(r'^verify_student/(?P<hash>\w+)',views.verify_student),
    url(r'^verify_faculty/(?P<hash>\w+)',views.verify_faculty),
    url(r'^search/$',views.search_page),
    url(r'^$', lambda r: HttpResponseRedirect('portal/')),
    url(r'^requestcontact/(?P<category>\w+)/(?P<contacttype>\w+)/(?P<userid>\d+)/$',views.requestcontact, name="requestcontact"),
    url(r'^request_update/(?P<reqtype>\w+)/(?P<reqid>\d+)/(?P<reqresponse>\w+)/$', views.request_update),
    url(r'^user_detail/(?P<userid>\d+)/(?P<categorypass>\w+)/$', views.user_detail, name="user_detail"),
    url(r'^interestprint/$', views.profile_page),
    url(r'^notification_read/$', views.notification_read),
    url(r'^delete_interest/(?P<interestid>\d+)/$', views.delete_interest),
    url(r'^editprofile/$', views.profile_page),
    url(r'^contactus/$',views.contactUs),
    url(r'^mentor_response/$', views.mentor_response),
    url(r'^photo/$',views.photo),
    url(r'^setting/$', views.setting_page),
    url(r'^profile/$', views.profile_page),
    url(r'^setting/$',views.setting_page_data),
    url(r'^forum/$',views.portal_main_page),
    url(r'^guestHouse/$', views.guestHouse_page),
    url(r'^deletePhoto/$',views.deletePhoto),
    url(r'^pass_change/(?P<hash>\w+)', views.pass_change),
    url(r'^alumniMeet2017/$', views.AlumniMeet),
    url(r'^travel/$', views.travelUpdate),
    url(r'^receipt/$', views.pdfGenerate)
    #url(r'^notifications/$', views.notifications),
    #url(r'^deletePhoto/$', views.deletePhoto),
    #url(r'^update/$', views.updateProfile),
]
