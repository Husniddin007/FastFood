# api/urls.py
from django.urls import path
from .views import (
    UserListView, UserDetailView,
    CategoryListView, CategoryDetailView,
    FoodListView, FoodDetailView,
    OrderListView, OrderDetailView, RestaurantListView
)

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),

    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),

    path('foods/', FoodListView.as_view(), name='food-list'),
    path('foods/<int:pk>/', FoodDetailView.as_view(), name='food-detail'),

    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),

    path('restaurants/', RestaurantListView.as_view(), name='restaurant-list'),
]
