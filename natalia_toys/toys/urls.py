from django.urls import path

from . import views


app_name = 'toys'
urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('toys', views.toys, name='toys'),
    path('new_toy', views.new_toy, name='new_toy'),
    path('delete_toy/<toy_id>', views.delete_toy, name='delete_toy'),
    path('edit_toy/<toy_id>', views.edit_toy, name='edit_toy'),
    path('toy_info/<toy_id>', views.toy_info, name='toy_info'),
    path('contacts', views.contacts, name='contacts'),
]
