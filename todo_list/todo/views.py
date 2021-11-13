from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Todo
from .serializers import *
from django.shortcuts import render
from django.conf import settings


def about(request):
    return render(request, 'todo/about.html', {'user': request.user, 'server_version': settings.SERVER_VERSION})


class TodoView(APIView):

    def get(self, request):
        todos = Todo.objects.filter(Q(author=request.user) | Q(public=True)).order_by(
            '-date_add', '-important')
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)


class TodoFilterView(APIView):
    def get(self, request):
        todos = Todo.objects.all()
        query_params = QuerySerializer(data=request.query_params)
        if query_params.is_valid():
            if query_params.data.get('status'):
                p1 = Q(status__in=query_params.data['status'])
                todos = todos.filter(p1)
            if query_params.data.get('important') is not  None:
                p2 = (Q(important=query_params.data['important']))
                todos = todos.filter(p2)
            if query_params.data.get('public'):
                p3 = (Q(public=query_params.data['public'][0]))
                todos = todos.filter(p3)
        else:
            return Response(query_params.errors, status=status.HTTP_400_BAD_REQUEST)
        todos = todos.filter(author=request.user).order_by('-date_add', '-important')
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)


class TodoDetailView(APIView):
    def get(self, request, todo_id):
        todo = Todo.objects.filter(pk=todo_id, public=True).first()
        if not todo:
            raise NotFound(f'Опубликованная заметка с id={todo} не найдена')
        serializer = TodoDetailSerializer(todo)
        return Response(serializer.data)


class TodoEditorView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        new_todo = TodoEditorSerializer(data=request.data)
        if new_todo.is_valid():
            new_todo.save(author=request.user)
            return Response(new_todo.data, status=status.HTTP_201_CREATED)
        else:
            return Response(new_todo.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, todo_id):
        todo = Todo.objects.filter(pk=todo_id, author=request.user).first()
        if not todo:
            raise NotFound(f'Статья с id={todo_id} для пользователя {request.user.username} не найдена')
        new_todo = TodoEditorSerializer(todo, data=request.data, partial=True)
        if new_todo.is_valid():
            new_todo.save()
            return Response(new_todo.data, status=status.HTTP_200_OK)
        else:
            return Response(new_todo.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, todo_id):
        todo = Todo.objects.filter(pk=todo_id, author=request.user).first()
        if not todo:
            raise NotFound(f'Статья с id={todo_id} для пользователя {request.user.username} не найдена')
        else:
            todo.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class CommentEditorView(APIView):
    """ Комментарий к статье """
    permission_classes = (IsAuthenticated,)

    def post(self, request, todo_id):
        """ Новый комментарий """
        author = AuthorSerializer(read_only=True)
        todo = Todo.objects.filter(pk=todo_id, public=True).first()
        if not todo:
            raise NotFound(f'Опубликованая заметка с id={todo_id} не найдена')
        new_comment = CommentAddSerializer(data=request.data)
        if new_comment.is_valid():
            new_comment.save(todo=todo, author=request.user)
            return Response(new_comment.data, status=status.HTTP_201_CREATED)
        else:
            return Response(new_comment.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id):
        """ Удалить комментарий """
        comment = Comment.objects.filter(pk=comment_id, author=request.user)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentView(APIView):

    def get(self, request):
        """ Получить коментарии статей для блога """
        comments = Comment.objects.all().order_by('-date_add', 'message')
        serializer = CommentSerializer(comments, many=True)

        return Response(serializer.data)


# class CommentIdView(APIView):
#     def get(self, request, todo_id):
#         # todo = list(Todo.objects.filter(pk=todo_id, author=request.user).first())
#         comment = Comment.objects.filter(todo=todo_id)
#         if not comment:
#             raise NotFound(f'Заметка с id={todo_id} не найдена')
#         serializer = CommentSerializer(comment)
#         return Response(serializer.data)
