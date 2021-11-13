from django.urls import path
from . import views

app_name = 'todo'
urlpatterns = [
    path('todo/', views.TodoView.as_view(), name='todo-list'),
    path('todo/<int:todo_id>/', views.TodoDetailView.as_view(), name='todo'),
    path('todo/add/', views.TodoEditorView.as_view(), name='add'),
    path('todo/<int:todo_id>/save/', views.TodoEditorView.as_view(), name='save'),
    path('todo/<int:todo_id>/delete/', views.TodoEditorView.as_view(), name='delete'),
    path('comment/<int:todo_id>/add/', views.CommentEditorView.as_view(), name='comment_add'),
    path('comment/<int:comment_id>/delete/', views.CommentEditorView.as_view(), name='comment_del'),
    path('comment/', views.CommentView.as_view(), name='comment-list'),
    # path('comment/<int:todo_id>/', views.CommentIdView.as_view(), name='commentid-list'),
    path('filter/', views.TodoFilterView.as_view(), name='todo-filter'),
    path('about/', views.about, name='about')
]
