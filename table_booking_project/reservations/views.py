from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden, JsonResponse
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse
import datetime
from .models import Restaurant, Table, Booking
from .forms import RestaurantForm, TableForm, BookingForm


# ---------------------- ГЛАВНАЯ ----------------------
def home_view(request):
    """Главная страница"""
    return render(request, 'reservations/home.html')


# ---------------------- РЕСТОРАНЫ ----------------------
def restaurant_list(request):
    """Вывод всех ресторанов"""
    restaurants = Restaurant.objects.all()
    return render(request, 'reservations/restaurant_list.html', {'restaurants': restaurants})


def restaurant_detail(request, pk):
    """Вывод информации о ресторане и его столиках"""
    restaurant = get_object_or_404(Restaurant.objects.prefetch_related('tables'), pk=pk)
    return render(request, 'reservations/restaurant_detail.html', {'restaurant': restaurant})


@login_required
def restaurant_create(request):
    """Создание нового ресторана"""
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.owner = request.user
            restaurant.save()
            messages.success(request, "Ресторан успешно создан!")
            return redirect('restaurant_list')
    else:
        form = RestaurantForm()
    return render(request, 'reservations/restaurant_form.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser, login_url='/')
def my_restaurants(request):
    """Список ресторанов (только для администраторов)"""
    restaurants = Restaurant.objects.all()
    return render(request, 'reservations/my_restaurants.html', {'restaurants': restaurants})


@login_required
def restaurant_update(request, pk):
    """Редактирование ресторана (только владелец)"""
    restaurant = get_object_or_404(Restaurant, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES, instance=restaurant)
        if form.is_valid():
            form.save()
            messages.success(request, "Ресторан успешно обновлён!")
            return redirect('restaurant_detail', pk=pk)
    else:
        form = RestaurantForm(instance=restaurant)
    return render(request, 'reservations/restaurant_form.html', {'form': form})


@login_required
def restaurant_delete(request, pk):
    """Удаление ресторана (только для владельца)"""
    restaurant = get_object_or_404(Restaurant, pk=pk, owner=request.user)
    if request.method == 'POST':
        restaurant.delete()
        messages.success(request, "Ресторан успешно удалён!")
        return redirect('restaurant_list')
    return render(request, 'reservations/restaurant_confirm_delete.html', {'restaurant': restaurant})


# ---------------------- СТОЛИКИ ----------------------
@login_required
def table_create(request, restaurant_id):
    """Добавление столика в ресторан (только владелец)"""
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id, owner=request.user)
    if request.method == 'POST':
        form = TableForm(request.POST)
        if form.is_valid():
            table = form.save(commit=False)
            table.restaurant = restaurant
            table.save()
            messages.success(request, "Столик успешно добавлен!")
            return redirect('restaurant_detail', pk=restaurant_id)
    else:
        form = TableForm()
    return render(request, 'reservations/table_form.html', {'form': form, 'restaurant': restaurant})


@login_required
def table_delete(request, pk):
    """Удаление столика (только владелец ресторана)"""
    table = get_object_or_404(Table.objects.select_related('restaurant'), pk=pk)

    if table.restaurant.owner != request.user:
        return HttpResponseForbidden("Вы не можете удалить этот столик.")

    if request.method == 'POST':
        table.delete()
        messages.success(request, "Столик успешно удалён!")
        return redirect('restaurant_detail', pk=table.restaurant.pk)
    return render(request, 'reservations/table_confirm_delete.html', {'table': table})


def table_list(request):
    """Вывод всех доступных столиков"""
    tables = Table.objects.filter(is_available=True).select_related('restaurant')
    return render(request, 'reservations/table_list.html', {'tables': tables})


# ---------------------- БРОНИРОВАНИЕ ----------------------
@login_required
def booking_create(request):
    """Страница бронирования с выбором ресторана и доступных столиков"""
    restaurants = Restaurant.objects.all()

    if request.method == 'POST':
        table_id = request.POST.get("selected_table")
        booking_date = request.POST.get("booking_date")

        if not table_id or not booking_date:
            messages.error(request, "Выберите столик и дату бронирования!")
            return redirect('booking_create')

        table = get_object_or_404(Table, id=table_id)

        # Преобразуем строку в datetime (с осведомлённым временем)
        booking_date = timezone.make_aware(datetime.datetime.strptime(booking_date, "%Y-%m-%dT%H:%M"))

        # Проверка доступности столика
        if Booking.objects.filter(table=table, booking_date=booking_date).exists():
            messages.error(request, "Этот стол уже забронирован на указанное время.")
            return redirect('booking_create')

        # Проверка на прошедшую дату
        if booking_date < timezone.now():
            messages.error(request, "Вы не можете бронировать в прошлом!")
            return redirect('booking_create')

        booking = Booking.objects.create(user=request.user, table=table, booking_date=booking_date)
        messages.success(request, "Бронирование успешно создано!")
        return redirect('my_bookings')

    return render(request, 'reservations/booking_form.html', {'restaurants': restaurants})


@login_required
def get_available_tables(request, restaurant_id):
    """API для получения доступных столиков по ресторану"""
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    tables = Table.objects.filter(restaurant=restaurant, is_available=True)

    data = {"tables": [{"id": table.id, "seats": table.seats} for table in tables]}
    
    return JsonResponse(data)


@login_required
def my_bookings(request):
    """Список бронирований пользователя (только будущие брони)"""
    bookings = Booking.objects.filter(
        user=request.user,
        booking_date__gte=timezone.now()
    ).select_related('table__restaurant')
    return render(request, 'reservations/my_bookings.html', {'bookings': bookings})


@login_required
def booking_delete(request, pk):
    """Удаление брони (только своей)"""
    booking = get_object_or_404(Booking, pk=pk, user=request.user)

    if booking.booking_date < timezone.now():
        messages.error(request, "Нельзя удалить прошедшую бронь!")
        return redirect('my_bookings')

    if request.method == 'POST':
        booking.delete()
        messages.success(request, "Бронирование успешно удалено!")
        return redirect('my_bookings')

    return render(request, 'reservations/booking_confirm_delete.html', {'booking': booking})


@login_required
def restaurant_bookings(request):
    """Все бронирования владельца ресторана"""
    bookings = Booking.objects.filter(table__restaurant__owner=request.user).select_related('user', 'table')
    return render(request, 'reservations/restaurant_bookings.html', {'bookings': bookings})
