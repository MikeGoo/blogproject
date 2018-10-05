from ..models import Article,Category,Tags
from django import template
from django.db.models.aggregates import Count

register = template.Library()

@register.simple_tag
def get_recent_articles(num=5):
	return Article.objects.all().order_by('-create_time')[:num]

@register.simple_tag
def archives():
	return Article.objects.dates('create_time','month',order='DESC')

@register.simple_tag
def get_categorys():
	return Category.objects.annotate(articles_num=Count('article')).filter(articles_num__gt=0)

@register.simple_tag
def get_tags():
	return Tags.objects.annotate(articles_num=Count('article')).filter(articles_num__gt=0)
