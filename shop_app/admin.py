from django.contrib import admin
from .models import Category, Article, Comment, SearchHistory, Favorite

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug']
    list_display_links = ['id', 'title']
    prepopulated_fields = {'slug': ('title',)}


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'shopping', 'category', 'author', 'cost']
    list_display_links = ['id', 'title']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['shopping']
    list_editable = ['category', 'author', 'cost']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'article', 'author']
    list_filter = ['article']


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['id', 'article', 'user']
    list_display_links = ['id', 'user']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(SearchHistory)
admin.site.register(Favorite, FavoriteAdmin)

