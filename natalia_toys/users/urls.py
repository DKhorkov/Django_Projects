from django.urls import path, include

from . import views

app_name = 'users'
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('profile', views.profile, name='profile'),
    path('profile_changed', views.profile_changed, name='profile_changed'),
    path('password_changed', views.password_changed, name='password_changed'),
]
