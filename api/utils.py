from math import sqrt
from datetime import timedelta


def calculate_distance(lat1, lon1, lat2, lon2):
    distance = sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)
    return round(distance, 2)


def preparation_time_calcs(order):
    total_orders = order.order_foods.count() if hasattr(order,'order_foods') else 1
    preparation_time = 5 * (total_orders // 4 + 1)
    return timedelta(minutes=preparation_time)


def delivery_time_calcs(order):
    if not (order.latitude and order.longitude and order.restaurant.latitude and order.restaurant.longitude):
        return timedelta(0)
    distance = calculate_distance(
        order.lat, order.lon, order.destination_lat, order.destination_lon
    )
    delivery_time = distance * 3
    return timedelta(minutes=delivery_time)


def total_time(order):
    return preparation_time_calcs(order) + delivery_time_calcs(order)
