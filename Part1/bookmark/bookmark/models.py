from django.db import models

# Create your models here.

# Model DB의 테이블
# Field = DB의 컬럼

# 북마크
# 이름 => varchar
# URL주소 => varchar

class Bookmark(models.Model):
    name = models.CharField('이름', max_length=100)
    url = models.URLField('URL')
    created_at = models.DateTimeField('생성일시', auto_now_add=True)
    updated_at = models.DateTimeField('수정일시', auto_now=True)

    # 북마크 위에 클래스에서 지정한 이름으로 출력
    def __str__(self):
        return self.name

    # 필요 시 사용(주로 admin 시)
    class Meta:
        verbose_name = '북마크'
        verbose_name_plural = '북마크 목록'




