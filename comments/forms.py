from django import forms
from .models import Comment
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget


class CommentForm(forms.Form):
	# 用ckeditor为评论框设置富文本编辑器
	text = forms.CharField(widget=CKEditorWidget(config_name='comment_config'))
	article_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'id':'article_id'}))
	# 通过reply_comment_id字段传给view要回复的评论的id
	reply_comment_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'id':'reply_comment_id'}))