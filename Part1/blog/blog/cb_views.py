from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.models import Blog

class BlogListView(ListView):
    #model = Blog
    #queryset = Blog.objects.all().order_by('-created_at') # 역정렬
    queryset = Blog.objects.all()
    template_name = 'blog_list.html'
    paginate_by =  10
    ordering = ('-created_at', )

    def get_queryset(self):
        queryset = super().get_queryset()

        q = self.request.GET.get('q')

        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(content__icontains=q)
            )
        return queryset

class BlogDetailView(DetailView):
    model = Blog #Blog.objects.get(pk=값)
    template_name = 'blog_detail.html'
    # pk가 아닐 경우(선호안함)
    # pk_url_kwarg = 'id'

    # 쿼리셋 필터링
    # 조건에 맞는 객체만 조회하고 싶을 때 사용
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.filter(id_lte=50)

    # 단일 객체 조회 커스터마이징
    # 기본 get_object를 오버라이드해서 pk로 직접 조회
    # def get_object(self, query=None):
    #     object = super().get_object()
    #     object = self.model.objects.get(pk=self.kwargs.get('pk'))
    #
    #     return object

    # 템플릿에 추가 데이터 전달
    # 템플릿으로 넘길 데이터를 수정하거나 추가할 때 사용
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['test'] = 'CBV'
    #     return context

class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    template_name = 'blog_create.html'
    fields = ('category', 'title', 'content') # 기본 폼은 html에서 {{ form.as_p }}
    # success_url = reverse_lazy('cb_blog_list') # 정적 페이지인 목록 페이지인 경우 사용

    def form_valid(self, form):
        # 폼이 유효할 때 호출되는 메서드
        # 폼 데이터를 객체로 저장하되, 아직 DB에 저장하지 않음(commit=False)
        self.object = form.save(commit=False)

        # 현재 로그인한 사용자를 작성자로 설정
        self.object.author = self.request.user

        # 객체를 데이터베이스에 저장
        self.object.save()

        # 저장 후, 성공 URL로 리다이렉션
        return HttpResponseRedirect(self.get_success_url())

    # form_valid 함수 이후에 호출되는 함수.
    # 저장이 완료된 후 사용자를 리디렉션할 URL을 반환함.
    # reverse_lazy는 URL 이름(cb_blog_detail)과 파라미터(pk)를 사용해 URL 문자열을 생성하여 kwargs 변수에 담음.
    # self.object.pk는 방금 저장된 객체(Blog)의 기본키 값을 의미함.
    # models.py에 def get_absolute_url 함수가 아래 기능 대체
    # def get_success_url(self):
    #     return reverse_lazy('cb_blog_detail', kwargs={'pk': self.object.pk})


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    template_name = 'blog_update.html'
    fields = ('category', 'title', 'content')

    # 방법1. 404 오류, 작성자 본인만 수정 가능
    def get_queryset(self):
        queryset = super().get_queryset()

        # 관리자면 전체 글 조회
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(author=self.request.user)

    # 방법2. 404 오류, 작성자 본인만 수정 가능
    # def get_object(self, queryset=None):
    #     self.object = super().get_object(queryset)
    #
    #     if self.object.author !=self.request.user:
    #         raise Http404
    #     return self.object

    # def get_success_url(self):
    #     return reverse_lazy('cb_blog_detail', kwargs={'pk': self.object.pk})

class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog

    # 방법1. 404 오류, 작성자 본인만 수정 가능
    def get_queryset(self):
        queryset = super().get_queryset()

        # 관리자가 아니면 본인 글만 조회 (추천)
        if not self.request.user.is_superuser:
            queryset.filter(author=self.request.user)
        return queryset

    def get_success_url(self):
        return reverse_lazy('blog:list')





