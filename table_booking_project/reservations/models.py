from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Restaurant(models.Model):
    """Модель ресторана"""
    name = models.CharField("Название", max_length=100, db_index=True)
    address = models.CharField("Адрес", max_length=255, db_index=True)
    description = models.TextField("Описание", null=True, blank=True)
    photo = models.ImageField("Фото", upload_to='restaurant_photos/', blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="owned_restaurants")

    class Meta:
        verbose_name = "Ресторан"
        verbose_name_plural = "Рестораны"

    def __str__(self):
        return self.name


class Table(models.Model):
    """Модель столика в ресторане"""
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='tables', verbose_name="Ресторан")
    name = models.CharField("Название столика", max_length=50, default="Столик")  # ✅ Добавили название столика
    seats = models.PositiveIntegerField("Количество мест", default=2, db_index=True)  # ✅ Переименовано в `seats`
    is_available = models.BooleanField("Доступен", default=True, db_index=True)

    class Meta:
        verbose_name = "Столик"
        verbose_name_plural = "Столики"

    def __str__(self):
        return f"{self.name} ({self.seats} мест) - {self.restaurant.name}"


class Booking(models.Model):
    """Модель бронирования столика"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings', verbose_name="Пользователь")
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='bookings', verbose_name="Столик")
    booking_date = models.DateTimeField("Дата бронирования", db_index=True)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    status = models.CharField(
        "Статус",
        max_length=20,
        choices=[
            ("pending", "Ожидание"),
            ("confirmed", "Подтверждено"),
            ("canceled", "Отменено"),
        ],
        default="pending",
        blank=True
    )

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ["-booking_date"]
        constraints = [
            models.UniqueConstraint(fields=["table", "booking_date"], name="unique_booking")
        ]  # ✅ Современный способ вместо `unique_together`

    def __str__(self):
        return f"Бронь №{self.id} | {self.user.username} | {self.booking_date.strftime('%d-%m-%Y %H:%M')}"
