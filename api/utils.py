from datetime import timedelta


def preparation_time_calcs(order):
    preparation_time = 5 * (order.count() // 4 + 1)
    return timedelta(minutes=preparation_time)


def delivery_time_calcs(order):
    delivery_time = order.distance * 3
    return timedelta(minutes=delivery_time)


def total_time(order):
    return preparation_time_calcs(order) + delivery_time_calcs(order)
