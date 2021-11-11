from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User


def datetimetomorrow():
    return datetime.now() + timedelta(days=1)


class Todo(models.Model):
    STATUS = [
        (1, 'Активно'),
        (2, 'Отложено'),
        (3, 'Выполнено'),
    ]
    message = models.TextField(default='', verbose_name='Заметка')
    status = models.IntegerField(choices=STATUS, default=1, blank=True)
    author = models.ForeignKey(User, related_name='authors', on_delete=models.PROTECT, blank=True)
    date_add = models.DateTimeField(verbose_name='Дата публикции', default=datetimetomorrow, blank=True)
    public = models.BooleanField(default=False, verbose_name='Публичный')
    important = models.BooleanField(default=False, verbose_name='Важно!')

    def __str__(self):
        return self.message


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    todo = models.ForeignKey(Todo, related_name='comments', on_delete=models.CASCADE)
    date_add = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    message = models.TextField(default='', blank=True, verbose_name='Текст комментария')
    rating = models.BooleanField(default=False, verbose_name='Лайк')

    def __str__(self):
        return f'{self.rating}: {self.message or "Без комментариев"}'