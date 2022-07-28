"""URL-схемы для пользователей"""

from django.urls import path, include

from . import views


app_name = 'users'
urlpatterns = [
    # Включает URL авторизации по умолчанию
    path('', include('django.contrib.auth.urls')),  # аутентификационные URL-адреса по умолчанию, определенные Django
    path('register/', views.register, name='register'),  # Страница регистрации нового пользователя
]
