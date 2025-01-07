from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),

    path('catalog/', views.products, name = 'products'),
    path('catalog/<slug:category_slug>/', views.products, name = 'products_by_category'),
    path('product/<int:id>/<slug:slug>/', views.product, name = 'product'),

    path('cart/', views.cart, name = 'cart'),
    path('add/<int:productID>/', views.cart_add, name = 'cart_add'),
    path('delete/<int:productID>/', views.cart_delete, name = 'cart_delete'),
    path('append/<int:productID>/', views.cart_append, name = 'cart_append'),

    path('orders/', views.user, name = 'user'),
    path('registration/', views.registration, name = 'registration'),
    path('authorization/', views.authorization, name = 'authorization'),
    path('change/', views.change, name = 'change'),
    path('reset/', views.reset, name = 'reset'),
    path('exit/', views.exit, name = 'exit'),
    
    path('create_order/', views.create_order, name='create_order'),
    path('confirm_order/<int:orderID>/', views.confirm_order, name='confirm_order'),
]