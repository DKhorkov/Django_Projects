from django.shortcuts import render, redirect

from .models import Topic
from .forms import TopicForm, EntryForm
# Create your views here.


def index(request):
    """Домашняя страница приложения Learning Log."""
    return render(request, 'learning_logs/index.html')


def topics(request):
    """Выводит список тем."""
    topics = Topic.objects.all()
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


def topic(request, topic_id):
    """Выводи инфы по одной теме."""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.all()
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


def new_topic(request):
    """Определяет новую тему."""

    if request.method != 'POST':
        form = TopicForm()  # Поскольку данные не отправлялись, нужно создать пустую форму для заполнения.
    else:
        # Отправлены данные POST, поэтому их нужно обработать:
        form = TopicForm(data=request.POST)  # Информация, заполненная пользователем.
        if form.is_valid():
            form.save()  # Сохраняет форму, если она корректно заполнена (все поля по умолчанию заполнены).
            return redirect('learning_logs:topics')

    # Вывести пустую или недействительную форму:
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


def new_entry(request, topic_id):
    """Добавляет новую запись по конкретной теме."""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            # Сохранение заметки в переменную, а не сразу в БД, ибо нужно еще присвоить данной заметке топик,
            # к которому она относится, а только потом сохранить.
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context=context)
