from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import NewBlogForm
from .models import BlogPost

# Create your views here.


def main_page(request):
    """Представление основной страница сайта блогов."""
    blogs = BlogPost.objects.all()
    context = {'blogs': blogs}
    return render(request, 'blogs/main_page.html', context)


@login_required()
def new_blog(request):
    """Создание нового блога."""
    if request.method != 'POST':
        form = NewBlogForm()
    else:
        form = NewBlogForm(data=request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.owner = request.user
            blog.save()
            return redirect('blogs:main_page')

    context = {'form': form}
    return render(request, 'blogs/new_blog.html', context)


@login_required()
def edit_blog(request, blog_id):
    blog = BlogPost.objects.get(id=blog_id)
    if request.method != 'POST':
        form = NewBlogForm(instance=blog)
    else:
        form = NewBlogForm(instance=blog, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:main_page')

    # Если не включить в контекст "блог", то будет ошибка, ибо неоткуда брать id в edit_blog.html:
    context = {'form': form, 'blog': blog}
    return render(request, 'blogs/edit_blog.html', context)


@login_required()
def delete_blog(request, blog_id):
    """Удаление блога"""
    blog = BlogPost.objects.get(id=blog_id)
    blog.delete()
    return redirect('blogs:main_page')

