from django.db import models

# model:user
class User(models.Model):
	email = models.CharField(max_length = 200)
	password = models.CharField(max_length = 16)
	createTime = models.CharField(max_length = 200)

# model:music
class Music(models.Model):
	musicUrl = models.CharField(max_length = 200)
	musicName = models.CharField(max_length = 200)
	musicCode = models.CharField(max_length = 200)
	mp3 = models.CharField(max_length = 200)
	cover = models.CharField(max_length = 200)
	musicDescribe= models.CharField(max_length =200)
	musicType= models.CharField(max_length =20)

	musicPicUrl = models.CharField(max_length = 200)
	musicArtist = models.CharField(max_length = 200)
	musicLike = models.CharField(max_length = 200)
	musicPubTime = models.CharField(max_length = 200)
	musicAlbumtitle = models.CharField(max_length = 200)


# model:the music she loves
class UserLoveMusic(models.Model):
	userId = models.IntegerField()
	musicId = models.IntegerField()
	pairId = models.IntegerField()

# model:post
class Post(models.Model):
	title = models.CharField(max_length = 200)
	description = models.CharField(max_length = 2000)
	pubDate = models.CharField(max_length = 200)
	postType =  models.CharField(max_length = 1)


# model:pair
class Pair(models.Model):
	boyId = models.IntegerField(max_length = 100)
	girlId = models.IntegerField(max_length = 100)
	pairName = models.CharField(max_length = 200)