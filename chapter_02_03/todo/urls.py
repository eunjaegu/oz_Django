from django.urls import path
from todo import cb_views
from todo.cb_views import CommentCreateView, CommentDeleteView, CommentUpdateView

app_name = 'todo'

urlpatterns = [
    # 2. 클래스형 뷰 (Class-based View, CBV)
    path('', cb_views.TodoListView.as_view(), name='cbv_todo_list'),
    path('<int:pk>/', cb_views.TodoDetailView.as_view(), name='cbv_todo_info'),
    path('create/', cb_views.TodoCreateView.as_view(), name='cbv_todo_create'),
    path('<int:pk>/update/', cb_views.TodoUpdateView.as_view(), name='cbv_todo_update'),
    path('<int:pk>/delete/', cb_views.TodoDeleteView.as_view(), name='cbv_todo_delete'),
    path('comment/<int:todo_id>/create/',  CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/delete/',  CommentDeleteView.as_view(), name='comment_delete'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment_update')

]
