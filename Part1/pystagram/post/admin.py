from django.contrib import admin

from post.models import PostImage, Post


class PostImageInline(admin.TabularInline):
    model = PostImage
    fields = ['image']
    extra = 1 # 이미지 목록(파일선택) 하나만

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [
        PostImageInline
    ]


