from django.conf.urls import patterns, url

from musicApp import views

urlpatterns = patterns('',

	url(r'^$', views.IndexView.as_view(), name = 'music-list'),


	url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name = 'music-detail'),
	# ex:/musicApp/5/results/
	url(r'^(?P<user_id>\d+)/lovemusic/$', views.LoveMusicView.as_view(), name = 'userlovemusic-list'),

	url(r'^love/(?P<music_id>\d+)/$', views.love, name = 'music-love'),
	url(r'^unlove/(?P<music_id>\d+)/$', views.unlove, name = 'music-unlove'),
	
	url(r'^(?P<music_id>\d+)/download/', views.downloadMusic, name = 'downloadMusic'),
	url(r'^musichome/$', views.musicHome, name = 'music-home'),
	url(r'^onemusichome/(?P<music_id>\d+)/$', views.oneMusicHome, name = 'music-oneMusicHome'),
	url(r'^musichome/angularhome/$',views.angularHome, name = 'music-angularHome'),

	url(r'^musichome/userhome/(?P<user_id>\d+)/$',views.userHome, name = 'music-userHome'),
	url(r'^musichome/admin/$',views.admin, name = 'music-admin'),
	url(r'^register/$',views.register, name = 'music-register'),
	url(r'^login/$',views.login_view, name = 'music-login'),
	url(r'^logout/$',views.logout_view, name = 'music-logout'),
	)