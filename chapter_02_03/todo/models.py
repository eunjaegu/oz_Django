from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Todo(models.Model):
    COMPLETION_STATUS = [
        ('completed', '완료'),
        ('incomplete', '미완료'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자")
    title = models.CharField(max_length=50, verbose_name="제목")
    description = models.TextField(verbose_name="내용")
    start_date = models.DateTimeField(verbose_name="시작일")
    end_date = models.DateTimeField(verbose_name="종료일")
    #is_complete = models.BooleanField(default=False, verbose_name="완료 여부")
    is_complete = models.CharField(
        max_length=10, choices=COMPLETION_STATUS, default='incomplete', verbose_name="완료 여부"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")

    def __str__(self):
        return self.title
