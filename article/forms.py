from django import forms
from mdeditor.fields import MDTextFormField

from article.models import Article
from utils.bootstrap_form import BootStrapForm


class CreateArticleForm(BootStrapForm, forms.ModelForm):
    content = MDTextFormField(label='正文')

    class Meta:
        model = Article
        fields = ['title', 'content', 'status']
