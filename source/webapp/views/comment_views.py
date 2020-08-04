from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View

from webapp.forms import CommentForm, ArticleCommentForm
from webapp.models import Comment, Article
from django.views.generic import ListView, DeleteView, UpdateView


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
            return redirect('article_view', pk=article_pk)
        else:
            return render(request, 'article/article.html', context={'form': form, 'article': article})




class CommentCreateView(View):
    def get(self, request, *args, **kwargs):
        form = CommentForm()
        return render(request, 'comment/create.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = Comment.objects.create(
                author=form.cleaned_data['author'],
                text=form.cleaned_data['text'],
                article=form.cleaned_data['article'],

            )
            return redirect('comment_index', pk=comment.article.pk)
        else:
            return render(request, 'comment/create.html', context={'form': form})


#
# class CommentUpdateView(View):
#     def get(self, request, *args, **kwargs):
#         comment = get_object_or_404(Comment, pk=kwargs.get('pk'))
#         form = CommentForm(data={
#             'author': comment.author,
#             'text': comment.text,
#             'article': comment.article
#
#         })
#         return render(request, 'comment/update.html', context={'form': form, 'comment': comment})
#
#     def post(self, request, *args, **kwargs):
#         comment = get_object_or_404(Comment, pk=kwargs.get('pk'))
#         form = CommentForm(data=request.POST)
#         if form.is_valid():
#             comment.author = form.cleaned_data['author']
#             comment.text = form.cleaned_data['text']
#             comment.article = form.cleaned_data['article']
#             comment.save()
#             return redirect('comment_index')
#         else:
#             return render(request, 'comment/update.html', context={'form': form, 'comment': comment})
#


# class CommentDeleteView(View):
#     def get(self, request, *args, **kwargs):
#         comment = get_object_or_404(Comment, pk=kwargs.get('pk'))
#         return render(request, 'comment/delete.html', context={'comment': comment})
#     def post(self, request, *args, **kwargs):
#         comment = get_object_or_404(Comment, pk=kwargs.get('pk'))
#         comment.delete()
#         return redirect('comment_index')





class CommentUpdateView(UpdateView):
    model = Comment
    template_name = 'comment/update.html'
    form_class = ArticleCommentForm
    context_object_name = 'comment'

    def get_success_url(self):
        return reverse('article_view', kwargs={'pk': self.object.article.pk})




class CommentDeleteView(DeleteView):
    model = Comment

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('article_view', kwargs={'pk': self.object.article.pk})



#
# class CommentDeleteView(DeleteView):
#     model = Comment
#     template_name = 'comment/delete.html'
#     # form_class = CommentForm
#     # context_object_name = 'comments'
#
#     def get_success_url(self):
#         return reverse('comment_index')