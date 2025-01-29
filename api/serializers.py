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
    delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id',
                  'user',
                  'status',
                  'total_price',
                  'order_foods',
                  'delivery_address',
                  'distance_to_restaurant',
                  'delivery_time'
                  ]

    def get_distance_to_restaurant(self, obj):
        return obj.distance_to_restaurant_calc()

    def get_delivery_time(self, obj):
        total_time = obj.total_time()
        return str(total_time)

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        order_foods_data = validated_data.pop('order_foods')

        user, created = User.objects.get_or_create(id=user_data['id'], defaults=user_data)

        restaurant_data = validated_data.pop('restaurant', None)
        restaurant = Restaurant.objects.filter(id=restaurant_data['id']).first() if restaurant_data else None

        if not restaurant:
            restaurant = Restaurant.objects.first()

        order = Order.objects.create(user=user, restaurant=restaurant, **validated_data)

        for order_food_data in order_foods_data:
            food_data = order_food_data.pop('food')
            food = Food.objects.filter(id=food_data['id']).first()
            if not food:
                raise serializers.ValidationError(f"Food with id {food_data['id']} does not exist.")
            OrderFood.objects.create(order=order, food=food, quantity=order_food_data.get('quantity',1))

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
