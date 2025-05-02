from django.contrib import admin
from bookmark.models import Bookmark

# 북마크 목록 분류 추가 및 링크 접속
# @~ 이 부분 아래 북마크 생성 주석 처리 부분과 동일 기능
# django admin docs 로 구글링으로 admin 기능 검색
@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'url']    # 분류
    list_display_links = ['name', 'url']    # 링크 접속
    list_filter = ['name', 'url']           # 필터 적용


# 북마크 생성
# admin.site.register(Bookmark, BookmarkAdmin)

