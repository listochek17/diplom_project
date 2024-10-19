from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import Category, Article, Comment, ArticleViews, SearchHistory, Storage, Favorite
from .forms import LoginForm, RegisterForm, CommentForm, ArticleForm
from django.contrib.auth import authenticate, login, logout
from django.views.generic import UpdateView, DeleteView
from django.core.paginator import Paginator
from django.contrib.auth.models import User
import json


# Create your views here.


def home_view(request):
    # categories = Category.objects.all()
    articles = Article.objects.all()
    paginator = Paginator(articles, 4)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    history = []
    result = []
    if request.user.is_authenticated:
        history = request.user.search_history.all()
        for i in history:
            if i.text not in result:
                result.append(i.text)

    context = {
        'articles': articles,
        'history': result
    }
    return render(request, 'shop_app/index.html', context)


def feedback_view(request):
    return render(request, 'shop_app/feedback.html')


def category_view(request, slug):
    category = Category.objects.get(slug=slug)
    articles = Article.objects.filter(category=category)
    query = request.GET.get('sort', '')
    if query:
        articles = articles.order_by(query)
    context = {
        'category': category,
        'category_title': category.title,
        'articles': articles
    }
    return render(request, 'shop_app/categories.html', context)


def all_categories_page(request):
    articles = Article.objects.all()

    query = request.GET.get('sort', '')
    if query:
        articles = articles.order_by(query)

    paginator = Paginator(articles, 4)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    context = {
        'articles': articles,
        'category_title': 'Все категории'
    }
    return render(request, 'shop_app/categories.html', context)


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    comments = Comment.objects.filter(article=article)
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.article = article
            form.author = request.user
            form.save()
            return redirect('detail', pk=pk)
    else:
        form = CommentForm()

    context = {
        'article': article,
        'form': form,
        'comments': comments
    }
    return render(request, 'shop_app/detail.html', context)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')

    else:
        form = LoginForm

    context = {
        'form': form
    }
    return render(request, 'shop_app/login.html', context)


def registration_view(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    context = {
        'form': form
    }
    return render(request, 'shop_app/registration.html', context)


def user_logout(request):
    logout(request)
    return redirect('home')


def create_article_view(request):
    if request.method == 'POST':
        form = ArticleForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            return redirect('detail', pk=form.pk)
    else:
        form = ArticleForm()
    context = {
        'form': form
    }
    return render(request, 'shop_app/article_form.html', context)


class UpdateArticle(UpdateView):
    model = Article
    form_class = ArticleForm
    success_url = '/'
    template_name = 'shop_app/article_form.html'


def profile_view(request, username):
    user_obj = User.objects.get(username=username)
    qs = Article.objects.filter(author=user_obj)
    paginator = Paginator(qs, 4)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    total_comments = sum([article.comments.all().count() for article in qs])
    total_purchases = sum([article.shopping for article in qs])
    context = {
        'articles': articles,
        'user_obj': user_obj,
        'total_articles': qs.count(),
        'total_comments': total_comments,
        'total_purchases': total_purchases
    }
    return render(request, 'shop_app/profile.html', context)


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = 'shop_app/article_confirm_delete.html'
    success_url = '/'


def search(request):
    query = request.GET.get('q')
    history = []
    if request.user.is_authenticated:
        obj = SearchHistory(text=query, user=request.user)
        obj.save()
        history = request.user.search_history.all()

    articles = Article.objects.filter(title__iregex=query)
    context = {
        'articles': articles,
        'history': history
    }
    return render(request, 'shop_app/index.html', context)


def storage(request):
    storage_user = Storage.objects.filter(user=request.user)
    context = {
        'storage': storage_user
    }
    return render(request, 'shop_app/storage.html', context)


def favorite(request):
    favorite_article = Favorite.objects.filter(user=request.user)
    article = []
    for i in favorite_article:
        article.append(i.article)
    context = {
        'favorite_article': article,
        'category_title': 'Избранное'
    }
    return render(request, 'shop_app/favourit.html', context)


def remove_favorite(request, pk):
    article = Article.objects.get(pk=pk)
    favorite_articles = Favorite.objects.get(user=request.user, article=article)
    favorite_articles.delete()
    return redirect(request.META['HTTP_REFERER'])


def favorites_add(request, pk):
    article = Article.objects.get(pk=pk)
    favorite_article = Favorite.objects.create(user=request.user, article=article)
    favorite_article.save()
    return redirect(request.META['HTTP_REFERER'])


def storage_add(request, pk):
    product = Article.objects.get(pk=pk)
    storage_product = Storage.objects.filter(user=request.user, product=product)

    if storage_product:
        storage_product = storage_product.first()
        if storage_product:
            storage_product.quantity += 1
            storage_product.save()
            product.quantity -= 1
            product.save(update_fields=['quantity'])
    else:
        storage_product.create(user=request.user, product=product, quantity=1)
        product.quantity -= 1
        product.save(update_fields=['quantity'])

    return redirect(request.META['HTTP_REFERER'])


def storage_delete(request):
    storage_all = Storage.objects.filter(user=request.user)
    for i in storage_all:
            product = Article.objects.get(pk=i.product.pk)
            product.quantity += i.quantity
            product.save(update_fields=['quantity'])
    storage_all.delete()
    return redirect('storage')


def storage_product_plus(request, pk):
    product = Article.objects.get(pk=pk)
    storage_product = Storage.objects.get(product=product, user=request.user)
    if product.quantity != 0:
        product.quantity -= 1
        product.save(update_fields=['quantity'])
        storage_product.quantity += 1
        storage_product.save(update_fields=['quantity'])
        return redirect('storage')
    return redirect('storage')


def storage_product_minus(request, pk):
    product = Article.objects.get(pk=pk)
    storage_product = Storage.objects.get(product=product, user=request.user)
    if storage_product.quantity == 0:
        storage_product.delete()
    else:
        product.quantity += 1
        product.save(update_fields=['quantity'])
        storage_product.quantity -= 1
        storage_product.save(update_fields=['quantity'])
        return redirect('storage')
    return redirect('storage')


def storage_product_trash(request, pk):
    product = Article.objects.get(pk=pk)
    storage_product = Storage.objects.get(user=request.user, product=product)
    product.quantity += storage_product.quantity
    product.save(update_fields=['quantity'])
    storage_product.delete()
    return redirect('storage')


def buy(request):
    storage_user = Storage.objects.filter(user=request.user)
    for i in storage_user:
            i.product.shopping += i.quantity
            i.product.save(update_fields=['shopping'])
            i.delete()
    return redirect('storage')
