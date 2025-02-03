from rest_framework import serializers
from .models import User, Category, Food, Order, OrderFood, Restaurant


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id',
                  'username',
                  'email',
                  'role']


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


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'description',
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
    food = serializers.PrimaryKeyRelatedField(queryset=Food.objects.all())

    class Meta:
        model = OrderFood
        fields = ['id',
                  'food',
                  'quantity']


class OrderCreateSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    order_foods = OrderFoodSerializer(many=True)

    class Meta:
        model = Order
        fields = ['user', 'status', 'total_price', 'order_foods', 'delivery_address']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        order_foods_data = validated_data.pop('order_foods')
        restaurant = validated_data.pop('restaurant', None)

        user, created = User.objects.get_or_create(username=user_data['username'], defaults=user_data)
        if not restaurant:
            restaurant = Restaurant.objects.first()

        order = Order.objects.create(user=user, restaurant=restaurant, **validated_data)

        for order_food_data in order_foods_data:
            food_data = order_food_data.get('food')
            quantity = order_food_data.get('quantity')

            if not food_data:
                raise serializers.ValidationError('Food maʼlumotlari noto‘g‘ri!')

            food = Food.objects.filter(id=food_data['id']).first()
            if not food:
                raise serializers.ValidationError(f"Food ID {food_data['id']} topilmadi!")

            OrderFood.objects.create(order=order, food=food, quantity=quantity)

        order.total_price = sum([i.food.price * i.quantity for i in order.order_foods.all()])
        order.save()

        order.ready_time = self.calculate_ready_time(order)
        order.save()

        return order

    def calculate_ready_time(self, order):

        previous_orders = Order.objects.filter(restaurant=order.restaurant, status='pending').exclude(id=order.id)
        add_time = 0
        for prev_order in previous_orders:
            add_time += prev_order.total_time()

        time_new_order = order.total_time()

        total_time = time_new_order + add_time
        return total_time




class OrderDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    order_foods = OrderFoodSerializer(many=True)
    distance_to_restaurant = serializers.SerializerMethodField()
    delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'total_price', 'order_foods', 'delivery_address', 'distance_to_restaurant',
                  'delivery_time']

    def get_distance_to_restaurant(self, obj):
        return obj.distance_to_restaurant_calc()

    def get_delivery_time(self, obj):
        total_time = obj.total_time()
        previous_orders_time = self.previous_orders_time_calc(obj)
        total_time += previous_orders_time
        return str(total_time)

    def previous_orders_time_calc(self, obj):
        previous_orders = Order.objects.filter(restaurant=obj.restaurant, status='pending').exclude(id=obj.id)

        add_time = 0
        for prev_order in previous_orders:
            add_time += prev_order.total_time()

        return add_time
