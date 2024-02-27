from django.views.generic.list import ListView
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.core.cache import cache
from django.conf import settings
from django.urls import reverse_lazy

from .models import Article, Topic, Comment
from .mixins import AuthorMixin
from .forms import CommentForm

r = settings.DEFAULT_REDIS_CLIENT


class ArticleListView(ListView):
	topic_slug = None
	context_object_name = 'articles'
	template_name = 'articles/list.html'

	def dispatch(self, request, *args, topic_slug=None, **kwargs):
		if topic_slug:
			self.topic_slug = topic_slug
		return super().dispatch(request)

	def get_queryset(self):
		if self.topic_slug:
			topic = get_object_or_404(Topic, slug=self.topic_slug)
			key = f'qs_topic:{topic.id}'
			# check for cache with particular topic
			cache_result = cache.get(key)
			if not cache_result:
				qs = Article.active.all().filter(topic=topic)
				cache.set(f'qs_topic:{topic.id}', qs, 300)
				return qs
			return cache_result
		# if not topic check default cache
		key = 'qs'
		cache_result = cache.get(key)
		if not cache_result:
			qs = Article.active.all()
			cache.set('qs', qs, 300)
			return qs
		return cache_result


class ArticleCreateView(CreateView, PermissionRequiredMixin):
	model = Article
	permission_required = ['articles.add_article']
	fields = [
		'title', 'description',
		'topic', 'is_active', 'source',
	]
	template_name = 'articles/create.html'
	success_url = reverse_lazy('articles:list')


class ArticleDetailView(DetailView):
	slug = None
	context_object_name = 'article'
	template_name = 'articles/detail.html'

	def dispatch(self, request, slug, *args, **kwargs):
		self.slug = slug  
		return super().dispatch(request, slug, *args, **kwargs)

	def get_object(self, queryset=None):
		key = f'article:{self.slug}'
		cache_result = cache.get(key)
		if not cache_result or self.request.user.is_staff:
			article = get_object_or_404(Article, slug=self.slug)
			cache.set(key, article, 180)
			return article
		return cache_result

	def get_context_data(self, **kwargs):
		article = self.get_object()
		# increase views of the article by 1
		views = r.incr(f'article:{article.id}:views')
		# add this article to the sorted set of elements, 
		# if it doesn't exist, or increase its rating by 1
		r.zincrby('article_ranking', 1, article.id)
		context = super().get_context_data(**kwargs)
		form = CommentForm()
		context['form'] = form  
		context['views'] = views
		return context

	def post(self, request, slug, *args, **kwargs):
		article = self.get_object()
		form = CommentForm(data=request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.article = article
			comment.author = request.user  
			comment.save()
			return redirect(article.get_absolute_url())
		context = self.get_context_data(**kwargs)
		return self.render_to_response(context)


class ArticleEditView(UpdateView, PermissionRequiredMixin):
	permission_required = ['articles.edit_article']
	model = Article  
	template_name = 'articles/edit.html'
	fields = [
		'title', 'description',
		'is_active', 'topic', 
		'source',
	]

	def get_success_url(self):
		article = self.object
		return article.get_absolute_url()


class ArticleDeleteView(View, PermissionRequiredMixin):
	permission_required = ['articles.delete_article']	

	def dispatch(self, request, pk, *args, **kwargs):
		return self.delete(request, pk)

	def delete(self, request, pk):
		article = get_object_or_404(Article, id=pk)
		article.delete()
		return redirect('articles:list')


class CommentEditView(UpdateView, AuthorMixin):
	model = Comment
	fields = ['body']
	template_name = 'comments/edit.html'

	def get_success_url(self):
		article = self.object.article
		return article.get_absolute_url()


class CommentDeleteView(AuthorMixin, View):
	object = None
	pk = None

	def get_object(self):
		self.object = get_object_or_404(Comment, id=self.pk)
		return self.object

	def dispatch(self, request, pk, *args, **kwargs):
		self.pk = pk
		super().dispatch(request, *args, **kwargs)
		return self.delete(request)

	def delete(self, request):
		comment = self.get_object()
		article = comment.article
		comment.delete()
		return redirect(article.get_absolute_url())
