"""Определяет схемы URL для learning_logs."""

from django.urls import path  # Функция "path" связывает URL с представлениями.

from . import views

app_name = 'learning_logs'  # Данная переменная помогает этот urls.pyфайл от одноименных в других приложениях.
urlpatterns = [
    path('', views.index, name='index'),  # Домашняя страница
    path('topics', views.topics, name='topics'),  # Страница с темами
    path('topics/<topic_id>', views.topic, name='topic'),  # Страница с конкретной темой, выбранной пользователем
    path('new_topic', views.new_topic, name='new_topic'),  # Страница для добавления новой темы
    path('new_entry/<topic_id>', views.new_entry, name='new_entry'),  # Страница для добавления новой записи по теме
    path('edit_entry/<entry_id>', views.edit_entry, name='edit_entry'),  # Страница редактирования записи
]
