from django.urls import path

from blog import views

app_name = 'fb'

urlpatterns = [
    #1. 함수형 뷰 (Function-based View, FBV)
    path('', views.blog_list, name="list"),
    path('<int:pk>/', views.blog_detail, name="detail"),
    path('create/', views.blog_create, name='create'),
    path('<int:pk>/update/', views.blog_update, name='update'),
    path('<int:pk>/delete/', views.blog_delete, name='delete'),
]