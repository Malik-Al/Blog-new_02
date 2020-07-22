from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from webapp.forms import CommentForm
from webapp.models import Comment
from django.views.generic import ListView






class CommentIndexView(ListView):
    template_name = 'comment/index.html'
    model = Comment
    context_object_name = 'comments'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['comments'] = Comment.objects.all()
    #     return context





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



class CommentUpdateView(View):
    def get(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs.get('pk'))
        form = CommentForm(data={
            'author': comment.author,
            'text': comment.text,
            'article': comment.article

        })
        return render(request, 'comment/update.html', context={'form': form, 'comment': comment})

    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs.get('pk'))
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment.author = form.cleaned_data['author']
            comment.text = form.cleaned_data['text']
            comment.article = form.cleaned_data['article']
            comment.save()
            return redirect('comment_index')
        else:
            return render(request, 'comment/update.html', context={'form': form, 'comment': comment})



class CommentDeleteView(View):
    def get(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs.get('pk'))
        return render(request, 'comment/delete.html', context={'comment': comment})
    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs.get('pk'))
        comment.delete()
        return redirect('comment_index')