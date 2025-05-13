from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from blog.models import Blog, Comment

admin.site.register(Comment)

class CommentInline(admin.TabularInline):
    model = Comment
    fields = ['content', 'author']
    extra = 1


#@~ : 블로그 생성
@admin.register(Blog)
#admin.ModelAdmin -> SummernoteModelAdmin
class BlogAdmin(SummernoteModelAdmin):
    summernote_fields = ['content', ]
    # 관리자 댓글 관리
    inlines = [
        CommentInline
    ]


