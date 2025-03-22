from django import forms
from django.utils import timezone
from .models import Restaurant, Table, Booking

class RestaurantForm(forms.ModelForm):
    """Форма создания и редактирования ресторанов"""

    class Meta:
        model = Restaurant
        fields = ['name', 'address', 'description', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название ресторана'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите адрес ресторана'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Введите описание'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'photo': 'Загрузите изображение ресторана',
        }


class TableForm(forms.ModelForm):
    """Форма для добавления столиков в ресторан"""

    class Meta:
        model = Table
        fields = ['restaurant', 'seats']  # ✅ Исправлено `seats_count` → `seats`
        widgets = {
            'restaurant': forms.Select(attrs={'class': 'form-select'}),
            'seats': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': 'Количество мест'}),
        }
        help_texts = {
            'seats': 'Введите количество мест за столиком',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['restaurant'].queryset = Restaurant.objects.order_by('name')


class BookingForm(forms.ModelForm):
    """Форма бронирования столика"""

    table = forms.ModelChoiceField(
        queryset=Table.objects.filter(is_available=True).select_related('restaurant').order_by('restaurant__name'),
        empty_label="Выберите столик",
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    booking_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        initial=timezone.now(),
    )

    class Meta:
        model = Booking
        fields = ['table', 'booking_date']
        help_texts = {
            'booking_date': 'Выберите дату и время бронирования',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Устанавливаем ограничение: нельзя выбрать дату в прошлом
        now = timezone.localtime().strftime('%Y-%m-%dT%H:%M')  # ✅ Исправлено
        self.fields['booking_date'].widget.attrs['min'] = now

    def clean_booking_date(self):
        """Проверка, что дата бронирования не в прошлом"""
        booking_date = self.cleaned_data.get('booking_date')

        if booking_date:
            # Преобразуем `booking_date` в "осведомлённое" время
            booking_date = timezone.make_aware(booking_date, timezone.get_current_timezone())

            if booking_date < timezone.now():
                raise forms.ValidationError("Нельзя бронировать на прошедшие даты!")

        return booking_date

    def clean_table(self):
        """Проверка, что столик доступен на выбранную дату"""
        table = self.cleaned_data.get('table')
        booking_date = self.cleaned_data.get('booking_date')

        if table and booking_date:
            # Проверяем только дату, игнорируя точное время
            existing_booking = Booking.objects.filter(
                table=table,
                booking_date__date=booking_date.date()
            ).exists()
            if existing_booking:
                raise forms.ValidationError("Этот столик уже забронирован на указанную дату.")

        return table
