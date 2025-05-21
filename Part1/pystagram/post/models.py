import re

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from utils.models import TimestampModel

User = get_user_model()

class Post(TimestampModel):
    content = models.TextField('본문')
    user = models.ForeignKey(User, on_delete=models.CASCADE)    # 작성자 = 장고 사용자 모델 User.id

    # 관리자 페이지나 쉘에서 출력될 때 보여줄 문자열 정의
    def __str__(self):
        return f'[{self.user}] post'

    class Meta:
        verbose_name = '포스트'
        verbose_name_plural = '포스트 목록'

class PostImage(TimestampModel):
    # Post.id / images => post.image_set : 게시글에 있는 이미지
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField('이미지', upload_to='post/%Y/%m/%d')

    def __str__(self):
        return f'{self.post} image'


    class Meta:
        verbose_name = '이미지'
        verbose_name_plural = '이미지  목록'



#POST

# 이미지 (여러개)
# 게시글
# 작성자
# 작성일자
# 수정일자


# 태그 N : N
class Tag(TimestampModel):
    tag = models.CharField('태그', max_length=100)
    posts = models.ManyToManyField(Post, related_name='tags')

# 댓글
class Comment(TimestampModel):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    content = models.CharField('내용', max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post} | {self.user}'

class Like(TimestampModel):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)

    def __str__(self):
        return f'[like] {self.post} | {self.user}'




# 시그널 함수(post_save, pre_save, pre_delete, post_delete)는 클래스 밖에 정의하는 것이 원칙
# post_save : 저장 이후 실행되는 시그널 핸들러
# POST 모델이 저장될 때 아래 함수를 실행
@receiver(post_save, sender=Post)
def post_post_save(sender, instance, created, **kwargs):
    # Post 객체의 내용에서 해시태그를 추출 (정규표현식 사용)
    hashtags = re.findall(r'#(\w{1,100})(?=\s|$)', instance.content)

    # 기존 태그를 모두 제거 (ManyToMany 관계 초기화)
    instance.tags.clear()

    # 해시태그를 기반으로 Tag 객체를 가져오거나 새로 생성
    # 예시: tags = [(Tag 객체, False), (Tag 객체, True), ...]
    # [(< Tag: Tag object (1) >, True), (< Tag: Tag object (2) >, True)]
    tags = [
        Tag.objects.get_or_create(tag=hashtag)  # 반환값: (Tag 객체, 생성 여부)
        for hashtag in hashtags
    ]

    # 위에 튜플 리스트에서 Tag 객체만 추출
    # tags 리스트는 [(Tag 객체, 생성 여부)] 형태이므로, Tag 객체만 추출
    # [<Tag: Tag object (1)>, <Tag: Tag object (2)>]
    tags = [tag for tag, _ in tags]

    # 새 태그를 추가
    # 게시글과 새로 가져온 Tag 객체들을 ManyToMany 관계로 연결
    instance.tags.add(*tags)





