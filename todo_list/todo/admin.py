from django.contrib import admin
from .models import Todo, Comment
from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ['user']


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'status', 'author', 'date_add', 'public', 'important')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'date_add', 'todo', 'author', 'rating')
    readonly_fields = ('date_add',)
