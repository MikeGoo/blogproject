from django.contrib import admin

from .models import Article,Category,Tags,Author,View



class ArticleAdmin(admin.ModelAdmin):
	list_display = ['id','title','create_time','author']


class ViewAdmin(admin.ModelAdmin):
	list_display = ['view_num','content_object']

admin.site.register(Article,ArticleAdmin)
admin.site.register(Tags)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(View,ViewAdmin)