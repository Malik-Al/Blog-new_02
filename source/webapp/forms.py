from django import forms
from django.forms import widgets
from webapp.models import Category, Article, Comment


# class ArticleForm(forms.Form):
#     title = forms.CharField(max_length=200, required=True, label='Title')
#     author = forms.CharField(max_length=40, required=True, label='Author')
#     text = forms.CharField(max_length=3000, required=True, label='Text',
#                            widget=widgets.Textarea)
#     category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label='Category',
#                                       empty_label=None)



class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = []



#
# class CommentForm(forms.Form):
#     article = forms.ModelChoiceField(queryset=Article.objects.all(), required=True, label='Article',
#                                      empty_label=None)
#     author = forms.CharField(max_length=40, required=False, label='Author', initial='Аноним')
#     text = forms.CharField(max_length=400, required=True, label='Text', widget=widgets.Textarea)



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = []


# class ArticleCommentForm(forms.Form):
#     author = forms.CharField(max_length=40, required=False, label='Author', initial='Аноним')
#     text = forms.CharField(max_length=400, required=True, label='Text', widget=widgets.Textarea)



class ArticleCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = []

