from django.contrib import admin

from blog.models import Blog

#@~ : 블로그 생성
@admin.register(Blog)

class BlogAdmin(admin.ModelAdmin):
    pass
