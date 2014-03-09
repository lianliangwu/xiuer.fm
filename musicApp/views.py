from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.core import serializers

import logging

import sys
import json
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
	# return HttpResponse("You are loving on question %s." % music_id)
	music = get_object_or_404(Music, pk=music_id)

	# choose = request.POST.get["loveChoose",'True']
	try:
		love = UserLoveMusic(userId = 1,musicId = 1)
		love.save()
	except (KeyError,UserLoveMusic.DoesNotExist):
		return render(request,'musicApp/detail.html',{
			'music':music,
			'error_message':'You didnot select a choice.',
			})
	else:
		return HttpResponseRedirect(reverse('musicApp:music-list'))

# def downloadMusic view
def downloadMusic(request,music_id):
	object = Music.objects.get(id = 1)
	return HttpResponse("The music name:%s \n The music Url: %s" % (object.musicName,object.musicUrl))

# get music list
def getMyPlayList():
	musicList = list(Music.objects.all())
	myPlaylist ='['
	for music in musicList:
		mp3 = '/static/musicApp/music/'+ music.musicCode + '.mp3'
		cover = '/static/musicApp/images/'+ music.musicCode + '.jpg'
		myPlaylist = myPlaylist+'{\"mp3\":\"'+mp3+'\",\"cover\":\"'+cover+'\"},'
	last_myPlaylist = myPlaylist[0:-1]+']'
	# logging.debug(last_myPlaylist)
	return last_myPlaylist

# to the music home page
def musicHome(request):
	myPlaylist = getMyPlayList()
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
	type1UserMusicList = []
	type2UserMusicList = []
	type3UserMusicList = []

	for userLoveMusic in userLoveMusicList:
		logging.debug(userLoveMusic.musicId)
		music = Music.objects.get(id = int(userLoveMusic.musicId))
		logging.debug(music.musicName)
		if music.musicType == '1':
			type1UserMusicList.append(music)
		elif music.musicType == '2':
			type2UserMusicList.append(music)
		else:
			type3UserMusicList.append(music)

	return render(request,'musicApp/user_home.html',{
		'type1UserMusicList':type1UserMusicList,
		'type2UserMusicList':type2UserMusicList
		})

# admin:download music information
def admin(request):
	# logging
	logging.basicConfig(filename='musicAppLog.out',level=logging.DEBUG)
	
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
		for songList in songs:
			for song in songList:
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
						'error_message':'You didnot select a choice.',
						})
				else:
					return HttpResponseRedirect(reverse('musicApp:music-list'))

 









	