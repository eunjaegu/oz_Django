from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView

from post.forms import CommentForm
from post.models import Comment, Post


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        # 폼에서 입력한 내용으로 Comment 객체 생성 (아직 DB에 저장은 안 함)
        self.object = form.save(commit=False)

        # 현재 로그인한 사용자를 댓글 작성자로 지정
        self.object.user = self.request.user

        # URL 파라미터로 전달된 post_pk로 게시글(Post) 객체 DB 조회
        post = Post.objects.get(pk=self.kwargs.get('post_pk'))

        # 댓글과 게시물 연결
        self.object.post = post

        # 최종적으로 데이터베이스에 저장
        self.object.save()

        # 저장 후 리디렉션 (예: 메인 페이지)
        return HttpResponseRedirect(reverse('main'))




