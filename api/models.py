from django.db import models
from django.contrib.auth.models import AbstractUser

from api.utils import preparation_time_calcs, delivery_time_calcs, total_time, calculate_distance


class User(AbstractUser):
    ROLE_CHOOICE = (
        ("Admin", "admin"),
        ("Waiter", "waiter"),
        ("User", "user")
    )
    role = models.CharField(max_length=100, choices=ROLE_CHOOICE, default="user")
    groups = None
    user_permissions = None

    def __str__(self):
        return self.role


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    phone_number = models.CharField(max_length=13)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Food(models.Model):
    name = models.CharField(max_length=155)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="foods")
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='foods')

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOOICE = [
        ("Pending", "pending"),
        ("Accepted", "accepted"),
        ("Preparing", "preparing"),
        ("Delivered", "delivered"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=25, choices=STATUS_CHOOICE, default="pending")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    delivery_address = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    distance = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)

    def distance_to_restaurant_calc(self, *args, **kwargs):
        if not (self.latitude and self.longitude and self.restaurant):
            return None

        return calculate_distance(
            self.latitude, self.longitude,
            self.restaurant.latitude, self.restaurant.longitude
        )

    def preparation_time_calcs(self):
        return preparation_time_calcs(self)

    def delivery_time_calcs(self):
        return delivery_time_calcs(self)

    def total_time(self):
        return total_time(self)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class OrderFood(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_foods')
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity}x {self.food.name}  (Order {self.order.id})'
