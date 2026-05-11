from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='ecommerce_home'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('category/<str:category>/', views.product_category, name='product_category'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:pk>/<str:url>/', views.add_to_cart, name='add_to_cart'),
    path('decrement-cart/<int:pk>/<str:url>/', views.decrement_cart_count, name='decrement_cart_count'),
    path('remove-from-cart/<int:pk>/<str:url>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
]