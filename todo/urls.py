from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_todos, name='todo-list')
]