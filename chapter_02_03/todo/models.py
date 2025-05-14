from django.contrib.auth import get_user_model
from django.db import models
from io import BytesIO
from pathlib import Path

from PIL import Image

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
    thumbnail = models.ImageField(
        upload_to='todo/thumbnails', default='todo/no_image/NO-IMAGE.gif', null=True, blank=True, verbose_name="이미지"
    )
    completed_image = models.ImageField(upload_to='todo/completed_images', null=True, blank=True, verbose_name="수정 이미지")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.completed_image:
            return super().save(*args, **kwargs)

        image = Image.open(self.completed_image)
        image.thumbnail((100, 100))

        image_path = Path(self.completed_image.name)

        thumbnail_name = image_path.stem
        thumbnail_extension = image_path.suffix
        thumbnail_filename = f'{thumbnail_name}_thumbnail{thumbnail_extension}'

        if thumbnail_extension in ['.jpg', '.jpeg']:
            file_type = 'JPEG'
        elif thumbnail_extension == '.png':
            file_type = 'PNG'
        elif thumbnail_extension == '.gif':
            file_type = 'GIF'
        else:
            return super().save(*args, **kwargs)

        temp_thumb = BytesIO()
        image.save(temp_thumb, format=file_type)
        temp_thumb.seek(0)

        self.thumbnail.save(thumbnail_filename, temp_thumb, save=False)

        temp_thumb.close()
        return super().save(*args, **kwargs)

class Comment(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user}: {self.message}'


