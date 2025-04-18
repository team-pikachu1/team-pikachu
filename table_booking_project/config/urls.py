from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views  # Импорт стандартных вьюшек авторизации

urlpatterns = [
    path('', include('reservations.urls')),  # Главная страница из reservations
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # Пути для аккаунтов
    path('accounts/', include('django.contrib.auth.urls')),  # Стандартные пути авторизации Django

    # Пути для сброса пароля
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]

# Подключение медиа при DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
