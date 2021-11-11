from rest_framework import serializers
from .models import Todo, Comment
from django.contrib.auth.models import User
from datetime import datetime
from rest_framework.serializers import ModelSerializer, Serializer, DecimalField, ListField, ChoiceField, BooleanField


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'date_joined')


class TodoSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Todo
        fields = ('message', 'status', 'author', 'date_add', 'public', 'important')


class TodoDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Todo
        exclude = ('public',)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        try:
            date_add = datetime.strptime(ret['date_add'], '%Y-%m-%dT%H:%M:%S.%f')
        except:
            date_add = datetime.strptime(ret['date_add'], '%Y-%m-%dT%H:%M:%S')
        ret['date_add'] = date_add.strftime('%d %B %Y %H:%M:%S')
        return ret


class TodoEditorSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Todo
        fields = '__all__'
        read_only_fields = ['author', 'date_add', ]


class CommentAddSerializer(serializers.ModelSerializer):
    """ Добавление комментария """
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ['date_add', 'author', 'todo']


class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ['date_add', 'author', 'todo']


class QuerySerializer(Serializer):
    status = ListField(child=ChoiceField(choices=Todo.STATUS), required=False)
    important = BooleanField(required=False)
    public = BooleanField(required=False)
