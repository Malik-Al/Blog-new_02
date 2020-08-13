from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.http import urlencode
from webapp.forms import ArticleForm, CommentForm, SimpleSearchForm
from webapp.models import Article
from django.views.generic import TemplateView, ListView, DeleteView, UpdateView, CreateView





class IndexView(ListView):
    context_object_name = 'articles'
    model = Article
    template_name = 'article/index.html'
    ordering = ['-created_at']
    paginate_by = 3
    paginate_orphans = 1


    def get(self, request, *args, **kwargs):
        form = SimpleSearchForm(self.request.GET)
        query = None
        if form.is_valid():
            query = form.cleaned_data['search']
        self.form = form
        self.query = query
        return super().get(request, *args, **kwargs)


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        if self.query:
            context['query'] = urlencode({'search': self.query})
        context['form'] = self.form
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.query:
            queryset = queryset.filter(Q(title__icontains=self.query) | Q(author__icontains=self.query))
        return queryset





class ArticleView(TemplateView):
    template_name = 'article/article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article_pk = kwargs.get('pk')
        article = get_object_or_404(Article, pk=article_pk)
        context['article'] = article
        context['form'] = CommentForm()
        comments = article.comments.order_by('-created_at')
        paginator = Paginator(comments, 3, 0)
        page_numder = self.request.GET.get('page', 1)
        page = paginator.get_page(page_numder)
        context['paginator'] = paginator
        context['page_obj'] = page
        context['comments'] = page.object_list
        context['is_paginated'] = page.has_other_pages()
        return context




class ArticleCreateView(LoginRequiredMixin, CreateView):
    template_name = 'article/create.html'
    form_class = ArticleForm
    model = Article

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        return redirect('accounts:login')

    def get_success_url(self):
        return reverse('webapp:article_view', kwargs={'pk': self.object.pk})







class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    template_name = 'article/update.html'
    form_class = ArticleForm
    context_object_name = 'article'

    def get_success_url(self):
        return reverse('webapp:article_view', kwargs={'pk': self.object.pk})




class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'article/delete.html'
    model = Article
    context_key = 'article'
    success_url = reverse_lazy('webapp:index')



