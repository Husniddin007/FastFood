from django.contrib import admin
from .models import User, Category, Food, Order, OrderFood


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'email', 'is_active')
    search_fields = ('username', 'email')


admin.site.register(User, UserAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


admin.site.register(Category, CategoryAdmin)


class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_available', 'category')
    search_fields = ('name',)


admin.site.register(Food, FoodAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__username',)


admin.site.register(Order, OrderAdmin)


class OrderFoodAdmin(admin.ModelAdmin):
    list_display = ('order', 'food', 'quantity')


admin.site.register(OrderFood, OrderFoodAdmin)
