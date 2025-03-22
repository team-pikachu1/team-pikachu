# Generated by Django 5.1.7 on 2025-03-20 13:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('address', models.CharField(max_length=255, verbose_name='Адрес')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='restaurant_photos/', verbose_name='Фото')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owned_restaurants', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Ресторан',
                'verbose_name_plural': 'Рестораны',
            },
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seats_count', models.PositiveIntegerField(default=2, verbose_name='Количество мест')),
                ('is_available', models.BooleanField(default=True, verbose_name='Доступен')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tables', to='reservations.restaurant', verbose_name='Ресторан')),
            ],
            options={
                'verbose_name': 'Столик',
                'verbose_name_plural': 'Столики',
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_date', models.DateTimeField(verbose_name='Дата бронирования')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('status', models.CharField(choices=[('pending', 'Ожидание'), ('confirmed', 'Подтверждено'), ('canceled', 'Отменено')], default='pending', max_length=20, verbose_name='Статус')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='reservations.table', verbose_name='Столик')),
            ],
            options={
                'verbose_name': 'Бронирование',
                'verbose_name_plural': 'Бронирования',
                'ordering': ['-booking_date'],
            },
        ),
    ]
