from musicApp.models import Music
from musicApp.models import UserLoveMusic
from musicApp.models import Pair

from django.shortcuts import render

# format music list
def format(musicList):
	myPlaylist ='['
	for music in musicList:
		mp3 = '/static/musicApp/'+ music.musicUrl[7:]
		cover = music.musicPicUrl
		title = music.musicName.replace('"', '\\"')
		artist = music.musicArtist.replace('"', '\\"')
		id = str(music.id)
		myPlaylist = myPlaylist+'{\"mp3\":\"'+mp3+'\",\"title\":\"'+title+'\",\"id\":\"'+id+'\",\"cover\":\"'+cover+'\",\"artist\":\"'+artist+'\"},'
	formated_myPlaylist = myPlaylist[0:-1]+']'
	return formated_myPlaylist

# love channel
def lovechannel_view(request):
	user_id = request.user.id
	if user_id is not None:
		# one user id belong to only one pair
		try:
			pair = Pair.objects.get(boyId = user_id)
		except(Pair.DoesNotExist):
			pair = Pair.objects.get(girlId = user_id)
		lovechannel_list = []
		loves = UserLoveMusic.objects.filter(pairId = pair.id)
		for love in loves:
			music = Music.objects.get(id = int(love.musicId))
			if music.musicType != '2':
				# exclude the guangboju type-2
				lovechannel_list.append(music)
		myPlaylist = format(lovechannel_list)
		return render(request,'musicApp/user_music_home.html',{
			'myPlaylist2': myPlaylist, 
		})
	else :
		musicList = list(Music.objects.order_by('?')[0:12])
		myPlaylist = format(musicList)
		return render(request,'musicApp/user_music_home.html',{
			'myPlaylist2': myPlaylist, 
			# 'error_message':'请登录 xiuer.FM 查看红心MHz'
		})

# random channel
def randomchannel_view(request):
	user_id = request.user.id
	if user_id is not None:
		musicList = list(Music.objects.order_by('?')[0:8])
		myPlaylist = format(musicList)
		return render(request,'musicApp/user_music_home.html',{
			'myPlaylist2': myPlaylist, 
		})
	else :
		musicList = list(Music.objects.order_by('?')[0:8])
		myPlaylist = format(musicList)
		return render(request,'musicApp/user_music_home.html',{
			'myPlaylist2': myPlaylist, 
		})

# guangboju channel
def guanbojuchannel_view(request):
	user_id = request.user.id
	if user_id is not None:
		# 2: 广播剧类型
		musicList = list(Music.objects.filter(musicType = '2'))
		myPlaylist = format(musicList)
		return render(request,'musicApp/user_music_home.html',{
			'myPlaylist2': myPlaylist, 
		})
	else :
		musicList = list(Music.objects.order_by('?')[0:12])
		myPlaylist = format(musicList)
		return render(request,'musicApp/user_music_home.html',{
			'myPlaylist2': myPlaylist, 
			# 'error_message':'对不起，广播剧是妞妞听的'
		})

# love guangboju channel
def love_guanbojuchannel_view(request):
	user_id = request.user.id
	if user_id is not None:
		lovechannel_list = []
		try:
			pair = Pair.objects.get(boyId = user_id)
		except(Pair.DoesNotExist):
			pair = Pair.objects.get(girlId = user_id)
		loves = UserLoveMusic.objects.filter(pairId = pair.id)
		for love in loves:
			try:
				music = Music.objects.get(id = int(love.musicId),musicType = '2')
				lovechannel_list.append(music)
			except(Music.DoesNotExist):
				pass
		myPlaylist = format(lovechannel_list)
		return render(request,'musicApp/user_music_home.html',{
			'myPlaylist2': myPlaylist, 
		})
	else :
		musicList = list(Music.objects.order_by('?')[0:12])
		myPlaylist = format(musicList)
		return render(request,'musicApp/user_music_home.html',{
			'myPlaylist2': myPlaylist, 
			#'error_message':'对不起，广播剧是妞妞听的'
		})

