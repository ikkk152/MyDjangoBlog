from django.shortcuts import render
from django.views.generic import CreateView, ListView

from article.forms import CreateArticleForm
from article.models import Article


class CreateArticle(CreateView):
    template_name = 'article/create.html'
    model = Article
    form_class = CreateArticleForm


class ListArticle(ListView):
    model = Article
    template_name = 'article/list.html'
    context_object_name = 'articles'
    paginate_by = 10
