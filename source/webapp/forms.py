from django import forms
from django.forms import widgets
from webapp.models import CATEGORY_CHOICES


class ArticleForm(forms.Form):
    title = forms.CharField(max_length=200, required=True, label='Title')
    author = forms.CharField(max_length=40, required=True, label='Author')
    text = forms.CharField(max_length=3000, required=True, label='Text',
                           widget=widgets.Textarea)
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=False, label='Category')