from django.views.generic.base import View, TemplateResponseMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import PermissionRequiredMixin

from backend.apps.articles.models import Article
from .models import Content
from .utils import get_form, get_model


class CreateContentView(PermissionRequiredMixin, TemplateResponseMixin, View):
    template_name = 'content/create.html'
    permission_required = ['content.create_content']

    def get(self, request, article_id, model_name):
        model = get_model(model_name)
        form = get_form(model)
        article = get_object_or_404(Article, id=article_id)
        context = {'form': form, 'article': article}
        return self.render_to_response(context)

    def post(self, request, article_id, model_name):
        model = get_model(model_name)
        form = get_form(model, data=request.POST, files=request.FILES)
        article = get_object_or_404(Article, id=article_id)
        if form.is_valid():
            content = form.save()
            Content.objects.create(article=article, content=content)
            return redirect(article.get_absolute_url())
        context = {'form': form, 'article': article}
        return self.render_to_response(context)


class EditContentView(PermissionRequiredMixin, TemplateResponseMixin, View):
    template_name = 'content/edit.html'
    permission_required = ['content.edit_content']

    def get(self, request, article_id, model_name, content_id):
        model = get_model(model_name)
        content = get_object_or_404(model, id=content_id)
        article = get_object_or_404(Article, id=article_id)
        form = get_form(model, instance=content)
        context = {
            'form': form,
            'article': article,
            'model_name': model_name,
            'content': content,
        }
        return self.render_to_response(context)

    def post(self, request, article_id, model_name, content_id):
        model = get_model(model_name)
        content = get_object_or_404(model, id=content_id)
        article = get_object_or_404(Article, id=article_id)
        form = get_form(model, instance=content, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(article.get_absolute_url())
        context = {
            'article': article,
            'form': form,
            'model_name': model_name,
            'content': content,
        }
        return self.render_to_response(context)


class DeleteContentView(PermissionRequiredMixin, View):
    permission_required = ['content.delete_content']

    def post(self, request, article_id, content_id):
        item = get_object_or_404(Content, id=content_id)
        article = get_object_or_404(Article, id=article_id)
        item.content.delete()
        item.delete()
        return redirect(article.get_absolute_url())
