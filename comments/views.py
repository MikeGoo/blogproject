from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse
from blog.models import Article
from .forms import CommentForm
from .models import Comment

def article_comment(request):
	if request.method == 'POST':
		if request.user.is_authenticated:
			form = CommentForm(request.POST)
			if form.is_valid():
				comment = Comment()
				text = form.cleaned_data.get('text')
				reply_comment_id = form.cleaned_data.get('reply_comment_id')
				article_id = form.cleaned_data.get('article_id')
				article = get_object_or_404(Article,pk=article_id)
				if reply_comment_id != 0:
					comment.parent = Comment.objects.get(id=reply_comment_id)
					comment.reply_to = comment.parent.user
					if comment.parent.root:
						comment.root = comment.parent.root
					else:
						comment.root = comment.parent
				comment.text = text
				comment.user = request.user
				comment.article = article
				comment.save()
				data = {}
				data['status'] = 'SUCCESS'
				data['username'] = comment.user.username
				data['comment_time'] = comment.create_time.strftime("%Y-%m-%d %H:%M")
				data['text'] = comment.text
				return 	JsonResponse(data)
				# return redirect('blog:detail',article_pk)
			else:
				data = {}
				data['status'] = 'ERROR'
				return 	JsonResponse(data)
				# return render(request,'detail.html',context=context)
	return redirect('blog:detail')

def test_view(request):
	return render(request,'test.html',context={'value':10})