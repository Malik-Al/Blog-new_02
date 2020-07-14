from django.contrib import admin
from webapp.models import Article, Comment


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'category', 'created_at']
    list_filter = ['author', 'category']
    search_fields = ['title', 'text']
    fields = ['title', 'author', 'text',  'created_at', 'updated_at', 'category']
    readonly_fields = ['created_at', 'updated_at']


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)