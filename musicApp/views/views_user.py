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
from musicApp.models import Pair

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
	logging.debug('I LOVE LOVE LOVE LOVE LOVE YOU')
	user_id = request.user.id
	logging.debug(user_id)
	if user_id is not None:
		try:
			love = UserLoveMusic.objects.get(userId = user_id,musicId = int(music_id))
		except(UserLoveMusic.DoesNotExist):
			try:
				pair = Pair.objects.get(boyId = user_id)
			except(Pair.DoesNotExist):
				pair = Pair.objects.get(girlId = user_id)
			love2 = UserLoveMusic(userId = user_id,musicId = int(music_id),pairId = pair.id)
			love2.save()
		return HttpResponseRedirect(reverse('musicApp:music-userHome',args=(user_id,)))
	else :
		myPlaylist = getMyPlayList()
		return render(request,'musicApp/music_home.html',{
			'myPlaylist2': myPlaylist, 
			'error_message':'请重新登录 xiuer.FM'
		})

# def argument view3
def unlove(request,music_id):
	try:
		user_id = request.user.id
		if user_id is not None:
			UserLoveMusic.objects.filter(userId = user_id,musicId = int(music_id)).delete()
			return HttpResponseRedirect(reverse('musicApp:music-userHome',args=(user_id,)))
		else :
			myPlaylist = getMyPlayList()
			return render(request,'musicApp/music_home.html',{
				'myPlaylist2': myPlaylist, 
				'error_message':'请重新登录 xiuer.FM'
			})
	except (KeyError,UserLoveMusic.DoesNotExist):
		return render(request,'musicApp/error.html')

# def downloadMusic view
def downloadMusic(request,music_id):
	object = Music.objects.get(id = 1)
	return HttpResponse("The music name:%s \n The music Url: %s" % (object.musicName,object.musicUrl))

# get music list
def getMyPlayList():
	musicList = list(Music.objects.order_by('?')[0:8])
	myPlaylist ='['
	for music in musicList:
		
		mp3 = '/static/musicApp/'+ music.musicUrl[7:]
		# logging.debug(mp3)

		cover = music.musicPicUrl

		title = music.musicName.replace('"', '\\"')
		artist = music.musicArtist.replace('"', '\\"')
		id = str(music.id)

		myPlaylist = myPlaylist+'{\"mp3\":\"'+mp3+'\",\"title\":\"'+title+'\",\"id\":\"'+id+'\",\"cover\":\"'+cover+'\",\"artist\":\"'+artist+'\"},'
	
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
	user_id = request.user.id
	if user_id is not None:
		user = authenticate(username="zhaochengxiu", password="zhaochengxiu")
		myPlaylist = getMyPlayList()
		response = render(request,'musicApp/user_music_home.html',{
			'user':user,
			'myPlaylist2': myPlaylist, 
		})
		return response
	else :
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
	# guangboju list
	UserMusicList_C2 = []
	# loveguangboju list
	UserMusicList_C3 = []

	for userLoveMusic in userLoveMusicList:
		music = Music.objects.get(id = int(userLoveMusic.musicId))
		UserMusicList_C1.append(music)
		try:
			music = Music.objects.get(id = int(userLoveMusic.musicId), musicType = '2')
			UserMusicList_C3.append(music)
		except(Music.DoesNotExist):
			pass
	UserMusicList_C0 = Music.objects.order_by('?')[0:20]
	UserMusicList_C2 = Music.objects.filter(musicType = '2')

	return render(request,'musicApp/user_home.html',{
		'UserMusicList_C0':UserMusicList_C0,
		'UserMusicList_C1':UserMusicList_C1,
		'UserMusicList_C2':UserMusicList_C2,
		'UserMusicList_C3':UserMusicList_C3,
		})

# admin:download music information
def admin(request):
	# logging
	logging.basicConfig(filename='musicAppLog.out',level=logging.DEBUG)
	# logging.debug("123")
	
	while True:
		# get the online music play list
		# Light music:9
		# 华语:1 - xiu.FM:101
		# 八零:4 - xiu.FM:104
		channel_id = '4'
		url = 'http://douban.fm/j/mine/playlist?type=n&channel='+channel_id
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
		# logging.debug(songs)
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
			existMusic = None
			try:
				existMusic = Music.objects.get(musicName = title,musicArtist = artist,musicPubTime = public_time,musicAlbumtitle = albumtitle)
			except(Music.DoesNotExist,Music.MultipleObjectsReturned):
				# Not exist in data base 
				if existMusic is None:
					try:
						# musicType: xiuer.FM type
						music = Music(musicType=channel_id+100,musicPicUrl = picture,musicArtist = artist,musicUrl = url,musicName = title,musicLike = like,
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
					except (KeyError):
						return render(request,'musicApp/detail.html',{
							'music':music,
							'error_message':'download error.',
							})
	return HttpResponseRedirect(reverse('musicApp:music-list'))

# register
def register(request):
	if request.method == 'POST':
		username = request.POST['username']
		# email = request.POST['email']
		password = request.POST['password']
		username2 = request.POST['username2']
		pairname = request.POST['pairname']
		myPlaylist = getMyPlayList()
		try:
			# my account
			Existuser = User.objects.get(username = username2)
			if Existuser is not None:
				return render(request,'musicApp/music_home.html',{
					'myPlaylist2': myPlaylist, 
					'error_message':'用户名'+username2+'已被占用，请重新注册.',
					})

		except(User.DoesNotExist):
			user = User.objects.create_user(username2," ",password)
			user.save()
			try:
				# Ta account
				Existuser2 = User.objects.get(username = username)
				if Existuser2 is not None:
					return render(request,'musicApp/music_home.html',{
						'myPlaylist2': myPlaylist, 
						'error_message':'用户名'+username+'已被占用，请重新注册.',
						})
			except(User.DoesNotExist):
				# missing validate
				user2 = User.objects.create_user(username," ",password)
				user2.save()
				# new pair
				pair = Pair(boyId = user.id,girlId = user2.id,pairName = pairname)
				pair.save()
				# push user to session
				user_temp = authenticate(username=username, password=password)
				login(request, user_temp)

				response = render(request,'musicApp/user_music_home.html',{
					'user':user_temp,
					'myPlaylist2': myPlaylist, 
					})
				# push user to cookieuser2.username
				response.set_cookie('xiuerFM_username', user2.username)
				response.set_cookie('xiuerFM_password', user2.password)
				return response

# login
def login_view(request):
	# POST Method
	if request.method == 'POST':
		response = post_login(request)
	else:
		response = sso_login(request)
	return response

# POST LOGIN 正常填写表单post登录
def post_login(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is not None:
		if user.is_active:
			# if user.is_staff:
			# current donot check the staff permission
			if 1:
				# staff user allow login
				# push user to session
				login(request, user)
				# Redirect to a success page.
				myPlaylist = getMyPlayList()
				response = render(request,'musicApp/user_music_home.html',{
					'user':user,
					'myPlaylist2': myPlaylist, 
				})
				# push user to cookie
				response.set_cookie('xiuerFM_username', username)
				response.set_cookie('xiuerFM_password', password)
				return response
			else:
				# Return an 'invalid login' error message.
				myPlaylist = getMyPlayList()
				return render(request,'musicApp/music_home.html',{
						'myPlaylist2': myPlaylist, 
						'error_message':'该系统仅允许秀儿登录'
					})
	else:
		# Return an 'invalid login' error message.
		myPlaylist = getMyPlayList()
		return render(request,'musicApp/music_home.html',{
				'myPlaylist2': myPlaylist, 
				'error_message':'用户名或密码错误'
			})

# SSO LOGIN 根据cookie单点登录
def sso_login(request):
	# GET Method
	# first look up the cookie ,if user exist,then direct to the user_music_home ,else direct to  login page
	username = request.COOKIES.get('xiuerFM_username')
	password = request.COOKIES.get('xiuerFM_password')
	if username is not None and password is not None:
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				# Redirect to a success page.
				myPlaylist = getMyPlayList()
				return render(request,'musicApp/user_music_home.html',{
					'user':user,
					'myPlaylist2': myPlaylist, 
				})
		else:
			logging.debug('USER information ERROR')
			# Return an 'invalid login' error message.
			myPlaylist = getMyPlayList()
			return render(request,'musicApp/music_home.html',{
					'myPlaylist2': myPlaylist, 
					'error_message':'请登录 xiuer.FM'
				})
	else:
		# Return an 'invalid login' error message.
		myPlaylist = getMyPlayList()
		return render(request,'musicApp/music_home.html',{
				'myPlaylist2': myPlaylist, 
				'error_message':'请登录 xiuer.FM'
			})	

# logout
def logout_view(request):
	logout(request)
	# Redirect to a success page.
	myPlaylist = getMyPlayList()
	return render(request,'musicApp/music_home.html',{
				'myPlaylist2': myPlaylist, 
			})





 









	