from django.conf.urls import patterns,url
from mspviz import views

urlpatterns = patterns('',
	url(r'^$',views.index,name='index'),
	url(r'^listmsps/',views.listmsps,name='listmsps'),
	url(r'^msp/(?P<mspID>\w+)/$', views.msp, name = 'msp'),
	url(r'^party/(?P<partyID>\w+)/$',views.party,name = 'party'))