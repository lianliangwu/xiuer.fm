from musicApp.models import Music
from musicApp.models import UserLoveMusic

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
		lovechannel_list = []
		loves = UserLoveMusic.objects.filter(userId = user_id)
		for love in loves:
			music = Music.objects.get(id = int(love.musicId))
			lovechannel_list.append(music)
		myPlaylist = format(lovechannel_list)
		return render(request,'musicApp/user_music_home.html',{
			'myPlaylist2': myPlaylist, 
		})
	else :
		musicList = list(Music.objects.order_by('?')[0:12])
		myPlaylist = format(musicList)
		return render(request,'musicApp/music_home.html',{
			'myPlaylist2': myPlaylist, 
			'error_message':'请登录 xiuer.FM 查看红心MHz'
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
		return render(request,'musicApp/music_home.html',{
			'myPlaylist2': myPlaylist, 
		})
