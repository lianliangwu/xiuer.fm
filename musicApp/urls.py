from django.conf.urls import patterns, url

from musicApp import views

urlpatterns = patterns('',
	# ex:/musicApp/
	url(r'^$', views.IndexView.as_view(), name = 'music-list'),
	# ex:/musicApp/5/
	url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name = 'music-detail'),
	# ex:/musicApp/5/results/
	url(r'^(?P<user_id>\d+)/lovemusic/$', views.LoveMusicView.as_view(), name = 'userlovemusic-list'),
	# ex:
	url(r'^(?P<music_id>\d+)/love/', views.love, name = 'love'),
	url(r'^(?P<music_id>\d+)/download/', views.downloadMusic, name = 'downloadMusic'),
	url(r'^musichome/$', views.musicHome, name = 'music-home'),
	url(r'^musichome/angularhome/$',views.angularHome, name = 'music-angularHome'),
	url(r'^musichome/userhome/(?P<user_id>\d+)/$',views.userHome, name = 'music-userHome'),
	url(r'^musichome/admin/$',views.admin, name = 'music-admin'),
	)