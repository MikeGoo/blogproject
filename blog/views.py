from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse
from .models import Article,Tags,Category,Tags,LoginForm,RegForm
import markdown
from comments.forms import CommentForm
from django.views.generic import ListView,DetailView
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User


class IndexView(ListView):
	model = Article
	template_name = 'index.html'
	context_object_name = 'articles'
	paginate_by = 10
	# 为首页设置页码
	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		paginator = context.get('paginator')
		page = context.get('page_obj')
		is_paginated = context.get('is_paginated')
		pagination_data = self.pagination_data(paginator,page,is_paginated)
		context.update(pagination_data)
		return context

	def pagination_data(self,paginator,page,is_paginated):
		if not is_paginated:
			return {}
		left = []
		right = []
		left_has_more = False
		right_has_more = False
		first = False
		last = False
		page_number = page.number
		total_pages = paginator.num_pages
		page_range = paginator.page_range

		if page_number == 1:
			right = page_range[page_number:page_number+2]
			if right[-1] < total_pages - 1:
				right_has_more = True

			if right[-1] < total_pages:
				last = True
		elif page_number == total_pages:
			left = page_range[(page_number-3) if (page_number-3)>0 else 0:page_number -1]
			if left[0] > 2:
				left_has_more = True

			if left[0] > 1:
				first = True

		else:
			left = page_range[(page_number-3) if (page_number-3)>0 else 0 :page_number-1]
			right = page_range[page_number:page_number+2]
			if right[-1] < total_pages - 1:
				right_has_more = True
			if right[-1] < total_pages:
				last = True

			if left[0] > 2:
				left_has_more = True
			if left[0] > 1:
				first = True

		data = {
			'left':left,
			'right':right,
			'left_has_more':left_has_more,
			'right_has_more':right_has_more,
			'first':first,
			'last':last
		}
		return data

class ArticleDetailView(DetailView):
	model = Article
	template_name = 'detail.html'
	context_object_name = 'article'

	def get(self,request,*args,**kwargs):
		# 通过设置cookie优化阅读数量自增。
		response = super(ArticleDetailView,self).get(request,*args,**kwargs)
		response.set_cookie('blog_%s' %self.kwargs.get('pk'),'True')
		if not request.COOKIES.get('blog_%s' %self.kwargs.get('pk')):
			self.get_object().increase_views()
		return response

	def get_object(self,query_set=None):
		# 通过markdown插件将markdown格式的文章转化为对应的HTML标签，从而使得文章支持markdown编辑。
		article = super(ArticleDetailView,self).get_object(queryset=None)
		article.content = markdown.markdown(article.content,
											extensions=[
												'markdown.extensions.extra', # 插件扩展
												'markdown.extensions.codehilite', # 语法高亮
												'markdown.extensions.toc'
											])
		return article

	def get_context_data(self,**kwargs):
		context = super(ArticleDetailView,self).get_context_data(**kwargs)
		# 实例化评论表单，并将reply_comment_id初始化为0
		comment_form = CommentForm(initial={'reply_comment_id':0,'article_id':self.get_object().pk})
		# 将root为空的评论过滤过来，设置到评论列表的最顶级
		comment_list = self.object.comment_set.filter(root=None)
		context.update({
			'comment_form':comment_form,
			'comment_list':comment_list,
			})
		return context

 # 通过年月过滤设置归档页面
class ArchivesView(IndexView):
	def get_queryset(self):
		year = self.kwargs.get('year')
		month = self.kwargs.get('month')
		return super(ArchivesView,self).get_queryset().filter(create_time__year=year,create_time__month=month).order_by('-create_time')

# 通过分类标签过滤设置分类页面
class CategoryView(ListView):
	model = Article
	template_name = 'index.html'
	context_object_name = 'articles'

	def get_queryset(self):
		# 关键字参数可以用self.kwargs.get('参数名')提取出来
		cate = get_object_or_404(Category,pk=self.kwargs.get('pk'))
		return super(CategoryView,self).get_queryset().filter(category=cate)

# 通过分类标签过滤设置标签页面
class TagView(IndexView):

	def get_queryset(self):
		tag = get_object_or_404(Tags,pk=self.kwargs.get('pk'))
		return super().get_queryset().filter(tag=tag)

# 设置博客展示页
class BlogView(ListView):
	model = Article
	template_name = 'index.html'
	context_object_name = 'articles'

	# 没有博客标签的话页面不显示任何东西。
	def get_queryset(self):
		try:
			cate = Category.objects.get(name='博客')
			return super().get_queryset().filter(category=cate)
		except:
			return []


def contact(request):
	return render(request,'contact.html')

def about(request):
	return render(request,'about.html')


def error_view(request,pk):
	article = Article.objects.get(pk=pk)
	return render(request,'error.html',{'article':article})

def login_view(request):
	# 通过from关键字获取跳转到登录页面之前的url
	previous_url = request.GET.get('from')
	if request.method == 'POST':
		login_form = LoginForm(request.POST)
		if login_form.is_valid():
			user = login_form.cleaned_data.get('user')
			login(request,user)
			return redirect(previous_url)
	else:
		login_form = LoginForm()
	# 登录页面有注册按钮可以跳转到注册页面，注册完之后也希望跳转到进入登录页面之前的页面，
	# 所以将登录页面之前的url传到登录页面，再通过登录页面的注册页面跳转链接传入到注册的view。
	context = {'form':login_form,'previous_url':previous_url}
	return render(request,'login.html',context=context)

def reg_view(request):
	if request.method == 'POST':
		# 获取登录之前的url
		previous_url = request.GET.get('from')
		reg_form = RegForm(request.POST)
		if reg_form.is_valid():
			# 获取用户名，邮箱，密码数据
			username = reg_form.cleaned_data['username']
			email = reg_form.cleaned_data['email']
			password = reg_form.cleaned_data['password']
			# 通过create_user创建新用户，通过这个方法创建之后会自动将密码设置为密文
			# 不然的话就需要通过user.set_password(password)方法创建密码字段。
			user = User.objects.create_user(username,email,password)
			user.save()

			# 用户登录
			user = authenticate(username=username,password=password)
			login(request,user)
			return redirect(previous_url)
	else:
		reg_form = RegForm()

	context={'reg_form':reg_form}
	return render(request,'register.html',context=context)

# 简陋个人中心
def personal_center_view(request):
	return render(request,'personal_center.html')

