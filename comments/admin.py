from django.contrib import admin 
from .models import Comment
from .forms import CommentForm


class CommentAdmin(admin.ModelAdmin):
	model = Comment

admin.site.register(Comment,CommentAdmin)