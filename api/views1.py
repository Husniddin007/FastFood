from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from .serializers import UserSerializer, CategorySerializer, FoodSerializer, OrderDetailSerializer, OrderCreateSerializer, RestaurantSerializer
from .utils import total_time


def run_sql_query(query, params=None):
    with connection.cursor() as cursor:
        cursor.execute(query, params or [])
        return cursor.fetchall()


class UserListView(APIView):
    def get(self, request):
        query = "SELECT id, username, email, role FROM api_user"
        users_data = run_sql_query(query)
        users = [{"id": user[0], "username": user[1], "email": user[2], "role": user[3]} for user in users_data]
        return Response(users)

    def post(self, request):
        query = "INSERT INTO api_user (username, email, role) VALUES (%s, %s, %s) RETURNING id"
        params = (request.data.get("username"), request.data.get("email"), request.data.get("role"))
        user_id = run_sql_query(query, params)
        return Response({"id": user_id[0][0]}, status=status.HTTP_201_CREATED)


class UserDetailView(APIView):
    def get(self, request, pk):
        query = "SELECT id, username, email, role FROM api_user WHERE id = %s"
        user_data = run_sql_query(query, [pk])
        if not user_data:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        user = {"id": user_data[0][0], "username": user_data[0][1], "email": user_data[0][2], "role": user_data[0][3]}
        return Response(user)

    def put(self, request, pk):
        query = "UPDATE api_user SET username = %s, email = %s, role = %s WHERE id = %s"
        params = (request.data.get("username"), request.data.get("email"), request.data.get("role"), pk)
        run_sql_query(query, params)
        return Response({"detail": "Updated successfully."})

    def delete(self, request, pk):
        query = "DELETE FROM api_user WHERE id = %s"
        run_sql_query(query, [pk])
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryListView(APIView):
    def get(self, request):
        query = "SELECT id, name, description FROM api_category"
        categories_data = run_sql_query(query)
        categories = [{"id": category[0], "name": category[1], "description": category[2]} for category in categories_data]
        return Response(categories)

    def post(self, request):
        query = "INSERT INTO api_category (name, description) VALUES (%s, %s) RETURNING id"
        params = (request.data.get("name"), request.data.get("description"))
        category_id = run_sql_query(query, params)
        return Response({"id": category_id[0][0]}, status=status.HTTP_201_CREATED)


class CategoryDetailView(APIView):
    def get(self, request, pk):
        query = "SELECT id, name, description FROM api_category WHERE id = %s"
        category_data = run_sql_query(query, [pk])
        if not category_data:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        category = {"id": category_data[0][0], "name": category_data[0][1], "description": category_data[0][2]}
        return Response(category)

    def put(self, request, pk):
        query = "UPDATE api_category SET name = %s, description = %s WHERE id = %s"
        params = (request.data.get("name"), request.data.get("description"), pk)
        run_sql_query(query, params)
        return Response({"detail": "Updated successfully."})

    def delete(self, request, pk):
        query = "DELETE FROM api_category WHERE id = %s"
        run_sql_query(query, [pk])
        return Response(status=status.HTTP_204_NO_CONTENT)


class FoodListView(APIView):
    def get(self, request):
        query = "SELECT id, name, price, category_id FROM api_food"
        foods_data = run_sql_query(query)
        foods = [{"id": food[0], "name": food[1], "price": food[2], "category_id": food[3]} for food in foods_data]
        return Response(foods)

    def post(self, request):
        query = "INSERT INTO api_food (name, price, category_id) VALUES (%s, %s, %s) RETURNING id"
        params = (request.data.get("name"), request.data.get("price"), request.data.get("category_id"))
        food_id = run_sql_query(query, params)
        return Response({"id": food_id[0][0]}, status=status.HTTP_201_CREATED)


class FoodDetailView(APIView):
    def get(self, request, pk):
        query = "SELECT id, name, price, category_id FROM api_food WHERE id = %s"
        food_data = run_sql_query(query, [pk])
        if not food_data:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        food = {"id": food_data[0][0], "name": food_data[0][1], "price": food_data[0][2], "category_id": food_data[0][3]}
        return Response(food)

    def put(self, request, pk):
        query = "UPDATE api_food SET name = %s, price = %s, category_id = %s WHERE id = %s"
        params = (request.data.get("name"), request.data.get("price"), request.data.get("category_id"), pk)
        run_sql_query(query, params)
        return Response({"detail": "Updated successfully."})

    def delete(self, request, pk):
        query = "DELETE FROM api_food WHERE id = %s"
        run_sql_query(query, [pk])
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderListView(APIView):
    def get(self, request):
        query = "SELECT id, user_id, restaurant_id, status, total_price, delivery_address FROM api_order"
        orders_data = run_sql_query(query)
        orders = [{"id": order[0], "user_id": order[1], "restaurant_id": order[2], "status": order[3], "total_price": order[4], "delivery_address": order[5]} for order in orders_data]
        return Response(orders)

    def post(self, request):
        query = "INSERT INTO api_order (user_id, restaurant_id, status, total_price, delivery_address) VALUES (%s, %s, %s, %s, %s) RETURNING id"
        params = (request.data.get("user_id"), request.data.get("restaurant_id"), request.data.get("status"), request.data.get("total_price"), request.data.get("delivery_address"))
        order_id = run_sql_query(query, params)
        return Response({"id": order_id[0][0]}, status=status.HTTP_201_CREATED)


class OrderDetailView(APIView):
    def get(self, request, pk):
        query = "SELECT id, user_id, restaurant_id, status, total_price, delivery_address FROM api_order WHERE id = %s"
        order_data = run_sql_query(query, [pk])
        if not order_data:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        order = {"id": order_data[0][0], "user_id": order_data[0][1], "restaurant_id": order_data[0][2], "status": order_data[0][3], "total_price": order_data[0][4], "delivery_address": order_data[0][5]}
        return Response(order)

    def put(self, request, pk):
        query = "UPDATE api_order SET user_id = %s, restaurant_id = %s, status = %s, total_price = %s, delivery_address = %s WHERE id = %s"
        params = (request.data.get("user_id"), request.data.get("restaurant_id"), request.data.get("status"), request.data.get("total_price"), request.data.get("delivery_address"), pk)
        run_sql_query(query, params)
        return Response({"detail": "Updated successfully."})

    def delete(self, request, pk):
        query = "DELETE FROM api_order WHERE id = %s"
        run_sql_query(query, [pk])
        return Response(status=status.HTTP_204_NO_CONTENT)


class RestaurantListView(APIView):
    def get(self, request):
        query = "SELECT id, name, address, phone_number FROM api_restaurant"
        restaurants_data = run_sql_query(query)
        restaurants = [{"id": restaurant[0], "name": restaurant[1], "address": restaurant[2], "phone_number": restaurant[3]} for restaurant in restaurants_data]
        return Response(restaurants)

    def post(self, request):
        query = "INSERT INTO api_restaurant (name, address, phone_number) VALUES (%s, %s, %s) RETURNING id"
        params = (request.data.get("name"), request.data.get("address"), request.data.get("phone_number"))
        restaurant_id = run_sql_query(query, params)
        return Response({"id": restaurant_id[0][0]}, status=status.HTTP_201_CREATED)
