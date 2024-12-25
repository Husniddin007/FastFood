from rest_framework import serializers
from .models import User, Category, Food, Order, OrderFood


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id',
                  'username',
                  'email',
                  'role']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'description'
        ]


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = [
            'id',
            'name',
            'price',
            'is_available',
            'category'
        ]


class OrderFoodSerializer(serializers.ModelSerializer):
    food = FoodSerializer()

    class Meta:
        model = OrderFood
        fields = ['id',
                  'food',
                  'quantity']


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    order_foods = OrderFoodSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id',
                  'user',
                  'status',
                  'total_price',
                  'order_foods',
                  'delivery_address',
                  'distance']
