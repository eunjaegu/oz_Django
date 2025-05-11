from django.contrib import admin

from blog.models import Blog, Comment

admin.site.register(Comment)

class CommentInline(admin.TabularInline):
    model = Comment
    fields = ['content', 'author']
    extra = 1


#@~ : 블로그 생성
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    # 관리자 댓글 관리
    inlines = [
        CommentInline
    ]


