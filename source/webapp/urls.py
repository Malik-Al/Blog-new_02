from django.contrib import admin
from django.urls import path, include


from webapp.views import IndexView, ArticleCreateView, ArticleView, ArticleUpdateView, ArticleDeleteView, \
    CommentCreateView, CommentIndexView, CommentUpdateView, CommentDeleteView, CommentForArticleCreateView



app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('article/create/', ArticleCreateView.as_view(), name='article_add'),
    path('article/<int:pk>', ArticleView.as_view(), name='article_view'),
    path('article/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_update'),
    path('article/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
    path('comment/add/', CommentCreateView.as_view(), name='comment_add'),
    path('comment/', CommentIndexView.as_view(), name='comment_index'),
    path('comment/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('article/<int:pk>/add-comment/', CommentForArticleCreateView.as_view(), name='article_comment_create')

    ]