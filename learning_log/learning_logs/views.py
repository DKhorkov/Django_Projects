from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.


def check_user(topic, request):
    """Проверяет, что тема принадлежит текущему пользователю.
    Если это не так, то будет вызвана ошибка 404 для недопущения работы с чужими данными."""
    if not topic.owner == request.user:
        raise Http404


def index(request):
    """Домашняя страница приложения Learning Log."""
    return render(request, 'learning_logs/index.html')


@login_required()
def topics(request):
    """Выводит список тем."""
    topics = Topic.objects.filter(owner=request.user).all()  # Темы видит только их создатель.
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


@login_required()
def topic(request, topic_id):
    """Выводи инфы по одной теме."""
    topic = Topic.objects.get(id=topic_id)

    check_user(topic, request)  # Проверка того, что тема принадлежит текущему пользователю.

    entries = topic.entry_set.all()
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required()
def new_topic(request):
    """Определяет новую тему."""

    if request.method != 'POST':
        form = TopicForm()  # Поскольку данные не отправлялись, нужно создать пустую форму для заполнения.
    else:
        # Отправлены данные POST, поэтому их нужно обработать:
        form = TopicForm(data=request.POST)  # Информация, заполненная пользователем.

        # Сохраняет форму, если она корректно заполнена (все поля по умолчанию заполнены):
        if form.is_valid():
            # Сохранение темы в переменную, а не сразу в БД, ибо нужно еще присвоить данной теме владельца,
            # к которому она относится, а только потом сохранить.
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')

    # Вывести пустую или недействительную форму:
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required()
def new_entry(request, topic_id):
    """Добавляет новую запись по конкретной теме."""
    topic = Topic.objects.get(id=topic_id)

    check_user(topic, request)

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


@login_required()
def edit_entry(request, entry_id):
    """Редактирование записи"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    check_user(topic, request)  # Проверка, что тема, к которой относится запись, принадлежит текущему пользователю

    if request.method != 'POST':
        form = EntryForm(instance=entry)  # Созданная форма будет не пустой, а с инфой из текущей записи.
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
