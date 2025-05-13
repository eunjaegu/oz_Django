from django.urls import path
from todo import views

app_name = 'fb'

urlpatterns = [
    # 1. 함수형 뷰 (Function-based View, FBV)
    path('todo/', views.todo_list, name='todo_list'),
    path('todo/create/', views.todo_create, name='todo_create'),
    path('todo/<int:pk>/', views.todo_info, name='todo_info'),
    path('todo/<int:pk>/update/', views.todo_update, name='todo_update'),
    path('todo/<int:pk>/delete/', views.todo_delete, name='todo_delete'),
]