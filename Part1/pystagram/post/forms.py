from django import forms
from django.forms import inlineformset_factory

from post.models import Post, PostImage, Comment
from utils.forms import BootstrapModelForm

# 게시글(Post)을 생성/수정할 때 사용하는 폼 클래스 정의
class PostForm(BootstrapModelForm):
    class Meta:
        model = Post
        fields = ('content', )


# 게시글 이미지(PostImage)를 위한 개별 이미지 입력 폼
class PostImageForm(BootstrapModelForm):
    class Meta:
        model = PostImage
        fields = ('image', )

PostImageFormSet = inlineformset_factory(
    Post,
    PostImage,
    form=PostImageForm,
    extra=1,
    can_delete=True,
    min_num=1,
    max_num=5
)

formset = [
    PostImageForm(),
    PostImageForm(),
    PostImageForm()
]

# Comment 모델에서 content 필드만 담음
class CommentForm(BootstrapModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
