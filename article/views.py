from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import CreateView, ListView

from article.forms import CreateArticleForm
from article.models import Article


class CreateArticle(CreateView):
    template_name = 'article/create.html'
    model = Article.get_markdown_content
    form_class = CreateArticleForm

    def form_valid(self, form):
        article = form.save(commit=False)
        article.user = self.request.user
        article.save()
        return JsonResponse({'success': True})

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors})

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ListArticle(ListView):
    model = Article
    template_name = 'article/list.html'
    context_object_name = 'articles'
    paginate_by = 8
