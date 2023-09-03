from django.urls import path
from . import views
urlpatterns = [
    path('', views.library, name='library'),
    path('category/<slug:category_slug>/', views.library, name='products_by_category'),
    path('<slug:category_slug>/<slug:product_slug>/', views.book_detail, name='product_detail'),
    path('search/', views.search, name='search'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
]