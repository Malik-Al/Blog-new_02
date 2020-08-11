from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View

from webapp.forms import CommentForm, ArticleCommentForm
from webapp.models import Comment, Article
from django.views.generic import ListView, DeleteView, UpdateView, CreateView


class CommentIndexView(ListView):
    template_name = 'comment/index.html'
    model = Comment
    context_object_name = 'comments'


class CommentForArticleCreateView(View):
    def post(self, request, *args, **kwargs):
        form = ArticleCommentForm(data=request.POST)
        article_pk = kwargs.get('pk')
        article = get_object_or_404(Article, pk=article_pk)
        if form.is_valid():
            Comment.objects.create(
                author=form.cleaned_data['author'],
                text=form.cleaned_data['text'],
                article=article

            )
            return redirect('webapp:article_view', pk=article_pk)
        else:
            return render(request, 'article/article.html', context={'form': form, 'article': article})





class CommentCreateView(CreateView):
    template_name = 'article/create.html'
    form_class = CommentForm
    model = Comment

    def get_success_url(self):
        return reverse('webapp:comment_index', kwargs={'pk': self.object.pk})





class CommentUpdateView(UpdateView):
    model = Comment
    template_name = 'comment/update.html'
    form_class = ArticleCommentForm
    context_object_name = 'comment'

    def get_success_url(self):
        return reverse('webapp:article_view', kwargs={'pk': self.object.article.pk})





class CommentDeleteView(DeleteView):
    model = Comment

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('webapp:article_view', kwargs={'pk': self.object.article.pk})



