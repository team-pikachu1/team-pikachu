import smtplib
from email.mime.text import MIMEText

# Данные для отправки
SMTP_SERVER = "smtp.office365.com"  # Используй официальный сервер
SMTP_PORT = 587
EMAIL_USER = "alikhan12320052005@outlook.com"
EMAIL_PASSWORD = "bqylrcopkmyxosqh"  # Пароль приложения, НЕ обычный пароль!

# Создание письма
msg = MIMEText("Тестовое письмо из Python. Если ты это читаешь — всё работает ✅")
msg["Subject"] = "Проверка отправки"
msg["From"] = EMAIL_USER
msg["To"] = EMAIL_USER

try:
    # Подключение к серверу
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.set_debuglevel(1)  # Включаем дебаг-режим (получишь логи)
    
    server.ehlo()  # Приветствие сервера
    server.starttls()  # Включение шифрования
    server.ehlo()  # Повторное приветствие после шифрования

    # Логин в почте
    server.login(EMAIL_USER, EMAIL_PASSWORD)

    # Отправка письма
    server.send_message(msg)
    server.quit()
    print("✅ Письмо успешно отправлено!")

except smtplib.SMTPAuthenticationError:
    print("❌ Ошибка аутентификации! Проверь пароль приложения и включение SMTP.")
except smtplib.SMTPException as e:
    print(f"❌ Ошибка SMTP: {e}")
except Exception as e:
    print(f"❌ Другая ошибка: {e}")
