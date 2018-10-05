from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
	path('comment/<int:article_pk>',views.article_comment,name='article_comment'),
	path('test/',views.test_view)
	]