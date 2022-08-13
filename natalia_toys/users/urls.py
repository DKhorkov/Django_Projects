from django.urls import path, include

from . import views
from .views import EmailVerify, MyLoginView

app_name = 'users'
urlpatterns = [
    # Переопределенное представление Логина, чтобы из него отправлялось сообщение на почту,
    # если пользователь не прошел верификацию. Также должно быть выше стандартных путей джанго, чтобы работало)
    # # "MyLoginView.as_view()" вместо "views.MyLoginView", ибо класс, а не функция:
    path('login/', MyLoginView.as_view(), name='login'),

    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('profile', views.profile, name='profile'),
    path('change_password', views.change_password, name='change_password'),
    path('profile_changed', views.profile_changed, name='profile_changed'),
    path('password_changed', views.password_changed, name='password_changed'),

    # Путь для обработки перехода по ссылки подтверждения электронной почты пользователем:
    path('verify_email/<uidb64>/<token>', EmailVerify.as_view(), name='verify_email'),

    # Путь для подтверждения электронной почты:
    path('confirm_email', views.confirm_email, name='confirm_email'),

    # Путь для завершения регистрации:
    path('registration_complete', views.registration_complete, name='registration_complete'),

    # Некорректная регистрации в случае, когда токен уже не может быть использован (устарел):
    path('invalid_verify', views.invalid_verify, name='invalid_verify'),

]
