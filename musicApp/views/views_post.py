from django.shortcuts import render

def post_view(request,user_id):
	userId = int(user_id)
	# logging.debug(userId)
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
