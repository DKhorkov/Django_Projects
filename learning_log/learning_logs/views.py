from django.shortcuts import render

from .models import Topic
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
