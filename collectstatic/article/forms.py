from django import forms

from article.models import Article
from utils.bootstrap_form import BootStrapForm
from markdownx.fields import MarkdownxFormField


class CreateArticleForm(BootStrapForm, forms.ModelForm):
    content = MarkdownxFormField(label='正文')

    class Meta:
        model = Article
        fields = ['title', 'content', 'status']
