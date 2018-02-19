"""saic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
import views
import portal.urls, portal.views

urlpatterns = [

  #login/logout
  url(r'^$', views.main_page),
  url(r'^gallery/$',views.gallery),
  url(r'^login/$',views.login_page),
  url(r'^logout/$', views.logout_page),

  #signup
  url(r'^signup/$', views.signup_page),
  url(r'^team/$',views.team_page),
  url(r'^chronicles/$',views.chronicles),
  url(r'^institute/$',views.abtinstitute,name='abtinstitute'),
  url(r'^centenary/$',views.abtcentenary,name='abtinstitute'),
  
  #web portal
  url(r'^portal/',include(portal.urls)),
  url(r'^portal/success/$', portal.views.success, name='order.success'),
  url(r'^portal/checkout/$',portal.views.checkout, name='order.checkout'),
  url(r'^portal/failure/$', portal.views.failure, name='order.failure'),


  # Serve static content.

  url(r'^admin/', include(admin.site.urls)),
  url('', include('social.apps.django_app.urls', namespace='social')),
  url('', include('django.contrib.auth.urls', namespace='auth')),
  url(r'^pass_recovery/$',views.pass_recovery),
] 
urlpatterns+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
