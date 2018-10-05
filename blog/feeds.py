from django.contrib.syndication.views import Feed

from .models import Article

class AllArticlesRssFeed(Feed):
	title = 'Django 博客教程演示项目'
	link = '/'
	description = 'Django 博客教程要是项目测试文章'

	def items(self):
		return Article.objects.all()

	def item_title(self,item):
		return '[%s] %s' % (item.category,item.title)

	def item_description(self,item):
		return item.content