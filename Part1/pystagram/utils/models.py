from django.db import models


class TimestampModel(models.Model):
    created_at = models.DateTimeField(verbose_name = '작성일자', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name = '수정일자', auto_now=True)

    class Meta:
        # 데이터 베이스 테이블 생성 안함.
        abstract = True