from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    (r'^order/', include('cart.urls')),
)