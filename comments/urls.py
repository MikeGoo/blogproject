from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
	path('comment',views.article_comment,name='article_comment'),
	path('test/',views.test_view,name='test')
	]