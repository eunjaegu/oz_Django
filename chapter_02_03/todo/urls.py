from django.urls import path
from todo import cb_views

app_name = 'todo'

urlpatterns = [
    # 2. 클래스형 뷰 (Class-based View, CBV)
    path('', cb_views.TodoListView.as_view(), name='cbv_todo_list'),
    path('<int:pk>/', cb_views.TodoDetailView.as_view(), name='cbv_todo_info'),
    path('create/', cb_views.TodoCreateView.as_view(), name='cbv_todo_create'),
    path('<int:pk>/update/', cb_views.TodoUpdateView.as_view(), name='cbv_todo_update'),
    path('<int:pk>/delete/', cb_views.TodoDeleteView.as_view(), name='cbv_todo_delete'),

]
