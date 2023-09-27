from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.CreateArticle.as_view(), name='create_article'),
    path('list/', views.ListArticle.as_view(), name='list_article'),
]
