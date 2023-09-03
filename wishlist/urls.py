from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.cart, name='cart'),
    path('<int:product_id>/', views.add_to_cart, name='add_cart'),
    path('delete/<int:id>/', views.remove_cart, name='remove_cart'),
    # path('delete/<int:product_id>/<int:cart_id>/', views.remove_cart, name='remove_cart')

]