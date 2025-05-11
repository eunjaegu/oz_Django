from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from utils.models import TimestampModel

User = get_user_model()

# 제목, 내용, 작성자, 작성일자, 수정일자, 카테코리, 썸네일이미지, 태그

class Blog(TimestampModel):
    #카테고리 종류
    # CHICES로 생성 시 셀렉트 박스로 생성됨.
    CATEGORY_CHOICES = (
        ('free', '자유'),
        ('travel', '여행'),
        ('cat', '고양이'),
        ('dog', '강아지'),  # 중복된 '고양이' 수정
    )
    category = models.CharField('카테고리', max_length=10, choices=CATEGORY_CHOICES, default='free')
    title = models.CharField('제목', max_length=100)
    content = models.TextField('본문')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # models.CASCADE => 연쇄 삭제
    # models.PROTECT => 삭제 불가(유저 삭제 시 블로그가 있으면 유저 삭제 불가)
    # models.SET_NULL, null=True => 널값을 넣음 => 유저 삭제 시 블로그의 author가 null이 됨.

    def __str__(self):
        # 카테고리 [free] 출력
        #return f'[{self.category}] {self.title[:10]}'
        # 카테고리 [자유]로 출력
        return f'[{self.get_category_display()}] {self.title}'

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})


    # 블로그 목록
    class Meta:
        verbose_name = '블로그'
        verbose_name_plural = '블로그 목록'

    # python manage.py makemigration
    # python manage.py migrate
    # python manage.py shell_plus
    # Blog.objects.filter(category='')
    # Blog.objects.filter(category='').update(category='free')


# 제목
# 본문
# 작성일자
# 수정일자
# 카테고리
# 작성자

# 댓글
class Comment(TimestampModel):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    content = models.CharField('본문', max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    #관리자 페이지에서 어느 블로그 글에 달린 댓글인지 확인
    def __str__(self):
        return f'{self.blog.title} 댓글'

    #관리자 페이지에서 모델 이름 한글로 설정
    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = '댓글 목록'
        ordering = ('-created_at', '-id')


# blog
# 댓글 내용
# 작성자
# 수정일자
# 작성일자




