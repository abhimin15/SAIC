from django.conf.urls import patterns, include, url
from cart import views

urlpatterns = patterns('',
    url(r'^checkout/$', views.checkout, name='order.checkout'),
    url(r'^success/$', views.success, name='order.success'),
    url(r'^failure/$', views.failure, name='order.failure'),
    url(r'^cancel/$', views.cancel, name='order.cancel'),
)
