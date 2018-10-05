from django.shortcuts import render,redirect
from django.contrib.auth import logout

def logout_view(request):
	previous_url = request.GET.get('from')
	context = {'previous_url':previous_url}
	# 用户注销
	logout(request)
	return redirect(previous_url)
