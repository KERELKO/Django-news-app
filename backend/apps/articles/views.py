from django.views.generic.list import ListView
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

from .models import Article, Topic, Comment
from .mixins import AuthorMixin
from .forms import CommentForm


class ArticleListView(ListView):
	topic_slug = None
	queryset = Article.active.all()
	context_object_name = 'articles'
	template_name = 'articles/list.html'

	def dispatch(self, request, *args, topic_slug=None, **kwargs):
		if topic_slug:
			self.topic_slug = topic_slug
		return super().dispatch(request)

	def get_queryset(self):
		qs = super().get_queryset()
		if self.topic_slug:
			topic = get_object_or_404(Topic, slug=self.topic_slug)
			return qs.filter(topic=topic)
		return qs


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
	model = Article
	context_object_name = 'article'
	template_name = 'articles/detail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		form = CommentForm()
		context['form'] = form  
		return context

	def post(self, request, slug, *args, **kwargs):
		article = get_object_or_404(Article, slug=slug)
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
