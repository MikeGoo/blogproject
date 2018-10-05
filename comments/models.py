from django.db import models
from django.utils.six import python_2_unicode_compatible
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

@python_2_unicode_compatible
class Comment(models.Model):
	text = RichTextField(config_name='comment_config')
	create_time = models.DateTimeField(auto_now_add=True)
	article = models.ForeignKey('blog.Article',on_delete=models.CASCADE)
	user = models.ForeignKey(User,related_name='comments_for_this_user', on_delete=models.DO_NOTHING)
	# 根回复
	root = models.ForeignKey('self', null=True, blank=True, related_name='comments_for_this_root',on_delete=models.DO_NOTHING)
	# 父级回复，即给哪一条评论回复
	parent = models.ForeignKey('self', null=True, blank=True,related_name='comments_for_this_parent', on_delete=models.DO_NOTHING)
	# 给谁回复
	reply_to = models.ForeignKey(User, null=True, blank=True, related_name='replies_for_this_user', on_delete=models.DO_NOTHING)


	def __str__(self):
		return self.text[:20]

	class Meta:
		ordering = ['-create_time']