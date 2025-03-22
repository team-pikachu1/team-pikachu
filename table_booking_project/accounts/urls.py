from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import register_view  # Используем только один view

app_name = "accounts"  # Это поможет избежать конфликтов

urlpatterns = [
    # 🔐 Вход и выход
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html'
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(
        next_page=reverse_lazy('accounts:login')  # После выхода → страница логина
    ), name='logout'),

    # 👤 Регистрация
    path('register/', register_view, name='register'),

    # 🔁 Сброс пароля
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset_form.html',
        email_template_name='accounts/password_reset_email.html',
        subject_template_name='accounts/password_reset_subject.txt',
        from_email='alikhan12320052005@outlook.com',  # ← вот здесь была ошибка: не хватало запятой
        success_url=reverse_lazy('accounts:password_reset_done')
    ), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html',
        success_url=reverse_lazy('accounts:password_reset_complete')
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),
]
