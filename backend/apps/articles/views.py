from django.views.generic.base import View, TemplateResponseMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.core.cache import cache
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.postgres.search import SearchVector

from .models import Article, Topic, Comment
from .mixins import AuthorMixin
from .forms import CommentForm, SearchForm
from .utils import get_cache, set_cache
from .tasks import article_published

r = settings.DEFAULT_REDIS_CLIENT
CACHE_TIMEOUT = settings.DEFAULT_CACHE_TIMEOUT


class ArticleSearchView(TemplateResponseMixin, View):
	query = None  
	template_name = 'articles/search.html'

	def post(self, request):
		query = None
		form = SearchForm(request.POST)
		if form.is_valid():
			query = form.cleaned_data['query']
			results = Article.active.annotate(
				search=SearchVector('title', 'description'),
			).filter(search=query)
		context = {
			'form': form,
			'query': query, 
			'results': results
		}
		return self.render_to_response(context)

	def get(self, request):
		form = SearchForm()
		context = {
			'form': form
		}
		return self.render_to_response(context)


class ArticleListView(TemplateResponseMixin, View):
	topic_slug = None 
	paginate_by = 2
	cache_key = None
	page = 1
	template_name = 'articles/list.html'

	def dispatch(self, request, topic_slug=None, *args, **kwargs):
		self.page = request.GET.get('page')
		if topic_slug:
			self.topic_slug = topic_slug
			self.cache_key = f'article_list_page:{self.page}|topic:{self.topic_slug}'
		else:
			self.cache_key = f'article_list_page:{self.page}'
		return super().dispatch(request, *args, **kwargs)

	def get_queryset(self):
		if self.topic_slug:
			topic = get_object_or_404(Topic, slug=self.topic_slug)
			queryset = Article.active.filter(topic=topic)
		else:
			queryset = Article.active.all()
		return queryset

	def get_context_data(self, **kwargs):
		context = kwargs
		qs = self.get_page()
		context['articles'] = qs
		context['page_obj'] = qs
		context['paginator'] = qs.paginator
		return context

	def get_page(self):
		paginator = self.get_paginator()
		qs = get_cache(self.cache_key)
		if not qs:
			qs = paginator.get_page(self.page)
			set_cache(key=self.cache_key, value=qs, time=CACHE_TIMEOUT)
		return qs

	def get_paginator(self):
		paginator = Paginator(
			self.get_queryset(), 
			self.paginate_by
		) 
		return paginator 

	def get(self, request, *args, **kwargs):
		return self.render_to_response(self.get_context_data())


class ArticleCreateView(PermissionRequiredMixin, CreateView):
	model = Article
	permission_required = ['articles.add_article']
	fields = [
		'title', 'description',
		'topic', 'is_active', 'source',
	]
	template_name = 'articles/create.html'
	success_url = reverse_lazy('articles:list')

	def form_valid(self, form):
		form = super().form_valid(form)
		if self.object.is_active:
			article_published.delay(self.object.pk)
		return form


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
			cache.set(key, article, CACHE_TIMEOUT)
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


class ArticleEditView(PermissionRequiredMixin, UpdateView):
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

	def form_valid(self, form):
		form = super().form_valid(form)
		if self.object.is_active:
			article_published.delay(self.object.pk)
		return form


class ArticleDeleteView(PermissionRequiredMixin, View):
	permission_required = ['articles.delete_article']	

	def dispatch(self, request, pk, *args, **kwargs):
		return self.delete(request, pk)

	def delete(self, request, pk):
		article = get_object_or_404(Article, id=pk)
		article.delete()
		return redirect('articles:list')


class CommentEditView(AuthorMixin, UpdateView):
	model = Comment
	fields = ['body']
	template_name = 'comments/edit.html'

	def get_success_url(self):
		article = self.object.article
		return article.get_absolute_url()


class CommentDeleteView(AuthorMixin, SingleObjectMixin, View):
	model = Comment

	def dispatch(self, request, *args, **kwargs):
		response = super().dispatch(request, *args, **kwargs)
		if isinstance(response, HttpResponse):
			return response
		return self.delete(request)

	def delete(self, request):
		comment = self.get_object()
		article = comment.article
		comment.delete()
		return redirect(article.get_absolute_url())