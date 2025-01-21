from rest_framework import serializers
from .models import User, Category, Food, Order, OrderFood, Restaurant


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
            'description',
            'restaurant'
        ]


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = [
            'id',
            'name',
            'price',
            'is_available',
            'category',
            'restaurant'
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
    distance_to_restaurant = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id',
                  'user',
                  'status',
                  'total_price',
                  'order_foods',
                  'delivery_address',
                  'distance_to_restaurant'
                  ]

    def get_distance_to_restaurant(self, obj):
        return obj.distance_to_restaurant_calc()

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        order_foods_data = validated_data.pop('order_foods')

        restaurant_data = validated_data.pop('restaurant', None)
        if restaurant_data:
            restaurant = Restaurant.objects.get(id=restaurant_data['id'])
        else:
            restaurant = Restaurant.objects.first()

        user = User.objects.create(**user_data)
        order = Order.objects.create(user=user, restaurant=restaurant, **validated_data)

        for order_food_data in order_foods_data:
            food_data = order_food_data.pop('food')
            food = Food.objects.get(id=food_data['id'])
            OrderFood.objects.create(order=order, food=food, **order_food_data)

        return order


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = [
            'id',
            'name',
            'address',
            'phone_number',
            'latitude',
            'longitude'
        ]
