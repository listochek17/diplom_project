from django.db import models
from django.contrib.auth.models import User

from django.template.defaultfilters import slugify

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название категории')
    slug = models.SlugField(null=True, verbose_name='Слаг')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Article(models.Model):
    title = models.CharField(max_length=100, verbose_name='Названия', unique=True)
    short_description = models.TextField(verbose_name='Краткое описания')
    full_description = models.TextField(verbose_name='Полное описания')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество товара')
    shopping = models.PositiveIntegerField(default=0, verbose_name='Количество покупок')
    preview = models.ImageField(upload_to='images/articles/previews/', blank=True, null=True, verbose_name='Фото товара')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', related_name='articles')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Продавец', related_name='articles',
                               null=True)
    slug = models.SlugField(blank=True)
    cost = models.PositiveIntegerField(default=0, verbose_name='Цена')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def price(self):
        return self.cost


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='comments')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статьи', related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username}: {self.article.title}'

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'

class ArticleViews(models.Model):
    session_id = models.CharField(max_length=150)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)


class SearchHistory(models.Model):
    text = models.CharField(max_length=500, verbose_name='Запрос поиска')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_history', verbose_name='User')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Запрос поиска'
        verbose_name_plural = 'Запросы поиска'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='User')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='Товар', null=True)

    def __str__(self):
        return self.user.username

class StorageQueryset(models.QuerySet):

    def total_price(self):
        a = 0
        product = []
        for i in self:
            product.append(i.product.cost)
        for price in product:
            a += price
        return a

    def total_quantity(self):
        if self:
            return sum([storage.quantity for storage in self])
        return 0


class Storage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Продукт', null=True)
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количеcтво')

    def __str__(self):
        return f'Корзина {self.user.username} Товар {self.product.title} Количество {self.quantity}'

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    objects = StorageQueryset().as_manager()

    def product_price(self):
        return round(self.product.price * self.quantity, 2)
