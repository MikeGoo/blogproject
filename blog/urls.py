from django.urls import path
from . import views

app_name = 'blog'

urlpatterns=[
	path('',views.IndexView.as_view(),name='index'),
	path('detail/<pk>',views.ArticleDetailView.as_view(),name='detail'),
	path('archives/<year>/<month>/',views.ArchivesView.as_view(),name='archives'),
	path('category/<pk>',views.CategoryView.as_view(),name='category'),
	path('tag/<pk>',views.TagView.as_view(),name='tag'),
	path('blog/',views.BlogView.as_view(),name='blog_view'),
	path('contact/',views.contact,name='contact'),
	path('about/',views.about,name='about'),
	path('error/<int:pk>',views.error_view,name='error'),
	path('login/',views.login_view,name='login'),
	path('register/',views.reg_view,name='register'),
	path('personal_center/',views.personal_center_view,name='personal_center'),
]