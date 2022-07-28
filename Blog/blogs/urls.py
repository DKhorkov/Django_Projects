"""URL для проекта blogs"""

from django.urls import path

from . import views

app_name = 'blogs'

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('new_blog', views.new_blog, name='new_blog'),
    path('edit_blog/<blog_id>', views.edit_blog, name='edit_blog'),
]