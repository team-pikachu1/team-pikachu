from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm  # Твоя кастомная форма на основе UserCreationForm

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Уже устанавливает пароль
            login(request, user)  # Авторизуем пользователя
            return redirect("home")  # Убедись, что есть url с именем "home"
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})
