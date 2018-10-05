from django import forms
from django.db import models
from django.urls import reverse
from django.utils.html import strip_tags
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
import markdown

class Article(models.Model):
	title = models.CharField(max_length=200)
	content = models.TextField()
	create_time = models.DateTimeField(auto_now_add=True)
	category = models.ForeignKey('Category',on_delete=models.CASCADE)
	tag = models.ManyToManyField('Tags',blank=True)
	abstract = models.CharField(max_length=200,blank=True)
	author = models.ForeignKey('Author',on_delete=models.CASCADE)

	def save(self,*args,**kwargs):
		if not self.abstract:
			md = markdown.Markdown(extensions=[
									'markdown.extensions.extra',
									'markdown.extensions.codehilite',])
			self.abstract = strip_tags(md.convert(self.content))[:54]
		super(Article,self).save(*args,**kwargs)

	def increase_views(self):
		ct = ContentType.objects.get(app_label='blog',model='article')
		view,created = View.objects.get_or_create(content_type=ct,object_id=self.pk)
		view.view_num += 1
		view.save()

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('blog:detail',kwargs={'pk':self.pk})

	def get_view(self):
		ct = ContentType.objects.get(app_label='blog',model='article')
		view,created = View.objects.get_or_create(content_type=ct,object_id=self.pk)
		return view.view_num

class Category(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name


class Tags(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

class Author(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

class View(models.Model):
	view_num = models.IntegerField(default=0)
	content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type','object_id')


class LoginForm(forms.Form):
	username_widget = forms.TextInput(attrs={'class':'form-control','placeholder':'请输入用户名'})
	password_widget = forms.PasswordInput(attrs={'class':'form-control','placeholder':'请输入密码'})
	username = forms.CharField(label='用户名',max_length=100,widget=username_widget)
	password = forms.CharField(label='密码',max_length=100,widget=password_widget)

	def clean(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		user = authenticate(username=username,password=password)

		if user is None:
			raise forms.ValidationError('用户名或密码输入不正确')
		else:
			self.cleaned_data['user'] = user
		return self.cleaned_data

class RegForm(forms.Form):
	username_widget = forms.TextInput(attrs={'class':'form-control','placeholder':'请输入用户名'})
	email_widget = forms.TextInput(attrs={'class':'form-control','placeholder':'请输入邮箱'})
	password_widget = forms.PasswordInput(attrs={'class':'form-control','placeholder':'请输入密码'})
	password_again_widget = forms.PasswordInput(attrs={'class':'form-control','placeholder':'请再输入一次密码'})

	username = forms.CharField(label='用户名',max_length=30,min_length=3,widget=username_widget)
	email = forms.EmailField(label='邮箱',widget=email_widget)
	password = forms.CharField(label='密码',min_length=6,widget=password_widget)
	password_again = forms.CharField(label='再输入一次密码',min_length=6,widget=password_again_widget)

	def clean_username(self):
		username = self.cleaned_data['username']
		if User.objects.filter(username=username).exists():
			raise forms.ValidationError('用户名已被注册')
		else:
			return username

	def clean_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError('邮箱已被注册')
		else:
			return email

	def clean_password_again(self):
		password = self.cleaned_data['password']
		password_again = self.cleaned_data['password_again']
		if password != password_again:
			raise forms.ValidationError('两次输入密码不一致')
		else:
			return password_again
	