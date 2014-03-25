from django.shortcuts import render
from django.utils import timezone 
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse

from musicApp.models import Post

def post_view(request,user_id):
	userId = int(user_id)
	postList = Post.objects.all()
	return render(request,'musicApp/user_post.html',{
		'postList':postList,
		})

def post_add_view(request):
	user_id = request.user.id
	if user_id is not None:
		if request.method == 'GET':
			return render(request,'musicApp/user_post_add.html')
		else:
			title = request.POST['title']
			description = request.POST['description']
			pubDate = timezone.now()
			postType = '1'
			post = Post(title=title,description=description,pubDate=pubDate,postType=postType)
			post.save()
		return HttpResponseRedirect(reverse('musicApp:music-post',args=(user_id,)))
	else:
		return render(request,'musicApp/user_post.html',{
			'error_message':'请重新登录 xiuer.FM'
		})