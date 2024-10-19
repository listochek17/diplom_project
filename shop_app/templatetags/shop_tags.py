from shop_app.models import Category, Article, Storage, Favorite
from django import template


register = template.Library()

@register.simple_tag()
def shop_categories():
    return Category.objects.all()

@register.simple_tag()
def shop_articles():
    return Article.objects.all()

@register.simple_tag()
def shop_storage(request):
    lst = []
    for i in Storage.objects.filter(user=request.user):
        lst.append(i.product)
    return lst

@register.simple_tag()
def shop_favorite(request):
    favorite_article = Favorite.objects.filter(user=request.user)
    l = []
    for i in favorite_article:
        l.append(i.article)
    if favorite_article:
        return l
    else:
        return []