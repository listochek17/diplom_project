from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('categories/', views.all_categories_page, name='all_categories'),
    path('categories/<slug:slug>/', views.category_view, name='category'),
    path('articles/add', views.create_article_view, name='create'),
    path('articles/<int:pk>/', views.article_detail, name='detail'),
    path('articles/<int:pk>/edit/', views.UpdateArticle.as_view(), name='edit'),
    path('articles/<int:pk>/delete/', views.ArticleDeleteView.as_view(), name='delete'),
    path('login/', views.login_view, name='login'),
    path('registration/', views.registration_view, name='registration'),
    path('logout/', views.user_logout, name='logout'),
    path('authors/<str:username>/', views.profile_view, name='profile'),
    path('search/', views.search, name='search'),
    path('storage/', views.storage, name='storage'),
    path('favorite/', views.favorite, name='favorite'),
    path('remove_favorites/<int:pk>', views.remove_favorite, name='remove_favorites'),
    path('favorite_category/<int:pk>', views.favorites_add, name='favorite_view'),
    path('storage_add/<int:pk>', views.storage_add, name='storage_add'),
    path('storage_delete/', views.storage_delete, name='storage_delete'),
    path('storage_product_plus/<int:pk>', views.storage_product_plus, name='storage_product_plus'),
    path('storage_product_minus/<int:pk>', views.storage_product_minus, name='storage_product_minus'),
    path('storage_product_trash/<int:pk>', views.storage_product_trash, name='storage_product_trash'),
    path('buy/', views.buy, name='buy')
]
