from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.core import serializers

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login ,logout

from musicApp.forms import UserForm

import logging

import sys
import os
import json
import subprocess
import urllib.request

from musicApp.models import Music
from musicApp.models import UserLoveMusic

# @list the music list
class IndexView(generic.ListView):
	model = Music

# @Parameter:primary key(hidden)	
# @list the detail music
class DetailView(generic.DetailView):
	model = Music

# @Parameter:user_id
# @list the love music of use[user_id]
class LoveMusicView(generic.ListView):
	model = UserLoveMusic

	def get_queryset(self):
		# logging.debug(self.kwargs['user_id'])
		return UserLoveMusic.objects.filter(userId = self.kwargs['user_id'])

# def argument view3
def love(request,music_id):
	try:
		user_id = request.session['user_id']
		logging.debug("WILL"+user_id)
		
		love = UserLoveMusic(userId = user_id,musicId = int(music_id))
		love.save()
	except (KeyError,UserLoveMusic.DoesNotExist):
		return render(request,'musicApp/error.html')
	return HttpResponseRedirect(reverse('musicApp:music-userHome',args=(user_id,)))

# def downloadMusic view
def downloadMusic(request,music_id):
	object = Music.objects.get(id = 1)
	return HttpResponse("The music name:%s \n The music Url: %s" % (object.musicName,object.musicUrl))

# get music list
def getMyPlayList():
	musicList = list(Music.objects.order_by('?')[0:12])
	myPlaylist ='['
	for music in musicList:
		
		mp3 = '/static/musicApp/'+ music.musicUrl[7:]
		# logging.debug(mp3)

		cover = music.musicPicUrl

		title = music.musicName.replace('"', '\\"')
		artist = music.musicArtist.replace('"', '\\"')

		myPlaylist = myPlaylist+'{\"mp3\":\"'+mp3+'\",\"title\":\"'+title+'\",\"cover\":\"'+cover+'\",\"artist\":\"'+artist+'\"},'
	
	last_myPlaylist = myPlaylist[0:-1]+']'
	# logging.debug(last_myPlaylist)
	return last_myPlaylist

# get music list :contain only one music
def getOneMusicPlayList(id):
	music = Music.objects.get(id = id)

	myPlaylist ='['
	mp3 = '/static/musicApp/'+ music.musicUrl[7:]
	cover = music.musicPicUrl
	title = music.musicName.replace('"', '\\"')
	artist = music.musicArtist.replace('"', '\\"')

	myPlaylist = myPlaylist+'{\"mp3\":\"'+mp3+'\",\"title\":\"'+title+'\",\"cover\":\"'+cover+'\",\"artist\":\"'+artist+'\"},'
	
	last_myPlaylist = myPlaylist[0:-1]+']'
	return last_myPlaylist

# to the music home page
def musicHome(request):
	myPlaylist = getMyPlayList()
	return render(request,'musicApp/music_home.html',{
		'myPlaylist2': myPlaylist,
		})

# listen one music
def oneMusicHome(request,music_id):
	myPlaylist = getOneMusicPlayList(id = int(music_id))
	return render(request,'musicApp/music_home.html',{
		'myPlaylist2': myPlaylist,
		})

# to the angular page
def angularHome(request):
	return render(request,'musicApp/example/index.html')

# to the user home page
def userHome(request,user_id):
	# get the user's music list
	# typeMusicList1 = list(UserLoveMusic.objects.filter(userId = self.kwargs['user_id']))
	userId = int(user_id)
	logging.debug(userId)
	userLoveMusicList = list(UserLoveMusic.objects.filter(userId = userId))
	# All music list:random
	UserMusicList_C0 = []
	# love music list
	UserMusicList_C1 = []

	for userLoveMusic in userLoveMusicList:
		music = Music.objects.get(id = int(userLoveMusic.musicId))
		UserMusicList_C1.append(music)
	UserMusicList_C0 = Music.objects.order_by('?')[0:20]

	return render(request,'musicApp/user_home.html',{
		'UserMusicList_C0':UserMusicList_C0,
		'UserMusicList_C1':UserMusicList_C1
		})

# admin:download music information
def admin(request):
	# logging
	logging.basicConfig(filename='musicAppLog.out',level=logging.DEBUG)
	logging.debug("123")
	
	while True:
		# get the online music play list
		url = 'http://douban.fm/j/mine/playlist?type=n&channel=0'
		#此时添加header，模拟浏览器访问，否则会报错：HTTPError: HTTP Error 403: Forbidden
		headers = {
		'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.114 Safari/537.36',
		}  
		req = urllib.request.Request(url, headers=headers)
		content = urllib.request.urlopen(req).read()
		# type = sys.getfilesystemencoding()  
		# content2 = content.decode("UTF-8",'ignore').encode(type)
		songs = json.loads(content.decode("utf-8"))['song']
		# log in file
		logging.debug(songs)
		# for songList in songs:
		for song in songs:
			# picture url
			picture = song['picture']
			# song artist
			artist = song['artist']
			# song url
			url = song['url']
			# song title
			title = song['title']
			# like or not
			like = song['like']
			# song public_time
			public_time = song['public_time']
			# albumtitle
			albumtitle = song['albumtitle']

			try:
				music = Music(musicPicUrl = picture,musicArtist = artist,musicUrl = url,musicName = title,musicLike = like,
					musicPubTime = public_time,musicAlbumtitle = albumtitle)
				# save the text information
				music.save()

				# 下载专辑
				songMp3 = 'music/' + title
				if not os.path.exists(songMp3):
				    subprocess.call([
				    	'wget','-r',
				    	'-A','.mp3',
				    	url
				    	])
			except (KeyError,Music.DoesNotExist):
				return render(request,'musicApp/detail.html',{
					'music':music,
					'error_message':'download error.',
					})
		
	return HttpResponseRedirect(reverse('musicApp:music-list'))

# register
def register(request):
	if request.method == 'POST':
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		user = User.objects.create_user(username, email, password)
		user.save()
	myPlaylist = getMyPlayList()
	return render(request,'musicApp/user_music_home.html',{
		'user':user,
		'myPlaylist2': myPlaylist, 
		})

# login
def login_view(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is not None:
		if user.is_active:
			login(request, user)
			# Redirect to a success page.
			myPlaylist = getMyPlayList()
			return render(request,'musicApp/user_music_home.html',{
				'user':user,
				'myPlaylist2': myPlaylist, 
			})
	else:
		# Return an 'invalid login' error message.
		myPlaylist = getMyPlayList()
		return render(request,'musicApp/user_music_home.html',{
				'myPlaylist2': myPlaylist, 
				'error_message':'用户名或密码错误'
			})

# logout
def logout_view(request):
	logout(request)
	# Redirect to a success page.
	myPlaylist = getMyPlayList()
	return render(request,'musicApp/music_home.html',{
				'myPlaylist2': myPlaylist, 
			})





 









	