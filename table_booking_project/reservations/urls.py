from django.urls import path
from .views import (
    home_view, 
    restaurant_list, restaurant_detail, restaurant_create, 
    my_restaurants, restaurant_update, restaurant_delete,
    table_list, table_create, table_delete,
    booking_create, my_bookings, booking_delete, restaurant_bookings,
    get_available_tables
)

urlpatterns = [
    path('', home_view, name='home'),

    # Рестораны
    path('restaurants/', restaurant_list, name='restaurant_list'),
    path('restaurants/<int:pk>/', restaurant_detail, name='restaurant_detail'),
    path('restaurants/create/', restaurant_create, name='restaurant_create'),
    path('restaurants/my/', my_restaurants, name='my_restaurants'),
    path('restaurants/<int:pk>/edit/', restaurant_update, name='restaurant_update'),
    path('restaurants/<int:pk>/delete/', restaurant_delete, name='restaurant_delete'),

    # Столики
    path('tables/', table_list, name='table_list'),
    path('tables/<int:restaurant_id>/create/', table_create, name='table_create'),
    path('tables/<int:pk>/delete/', table_delete, name='table_delete'),

    # Бронирование
    path('booking/create/', booking_create, name='booking_create'),
    path('my-bookings/', my_bookings, name='my_bookings'),
    path('booking/delete/<int:pk>/', booking_delete, name='booking_delete'),
    path('restaurant-bookings/', restaurant_bookings, name='restaurant_bookings'),

    # API для получения доступных столиков
    path('get_available_tables/<int:restaurant_id>/', get_available_tables, name='get_available_tables'),
]
