from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.forms import CommentForm
from blog.models import Blog, Comment

from blog.forms import BlogForm


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

class BlogDetailView(ListView):
    # DetailView -> ListView (댓글 페이지 네이션을 위해 변경, 디테일 뷰역할도 함)

    # comment에 list페이지를 만들고 블로그를 가져온다.
    model = Comment #Blog.objects.get(pk=값)


    # 최적화
    # prefetch_related(): ORM이 관련된 객체들을 미리 조회하여 캐싱함 -> 템플릿이나 뷰에서 추가 DB 요청 없이 사용 가능
    # 캐싱의 개념 (Django ORM 관점) : 처음 한 번만 DB에서 가져오고, 그 이후엔 메모리에 저장된 값을 계속 재사용하는 것
    # comment_set: 블로그 글과 연결된 댓글들을 미리 가져옴 (Blog → Comment)
    # comment_set__author: 각 댓글의 작성자 정보도 함께 가져옴 (Comment → User)
    #queryset = Blog.objects.all().prefetch_related('comment_set', 'comment_set__author')
    template_name = 'blog_detail.html'
    # pk가 아닐 경우(선호안함)
    # pk_url_kwarg = 'id'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(Blog, pk=kwargs.get('blog_pk'))
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(blog=self.object).prefetch_related('author')


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
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['blog'] = self.object
        return context

    # 코멘트 생성
    # def post(self, *args, **kwargs):
    #     comment_form = CommentForm(self.request.POST)
    #
    #     # True로 수정해서 값이 들어감을 확인해보기
    #     if not comment_form.is_valid():
    #         self.object = self.get_object()
    #         context = self.get_context_data(object=self.object)
    #         context['comment_form'] = comment_form
    #         return self.render_to_response(context)
    #
    #     # 로그인 여부
    #     if not self.request.user.is_authenticated:
    #         raise Http404
    #
    #     comment = comment_form.save(commit=False)
    #     comment.blog = self.get_object()
    #     #comment.blog_id = self.kwargs['pk']
    #     comment.author = self.request.user
    #     comment.save()
    #
    #     return HttpResponseRedirect(reverse_lazy('blog:detail', kwargs={'pk': self.kwargs['pk']}))



class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    template_name = 'blog_form.html'
    form_class = BlogForm
    #fields = ('category', 'title', 'content') # 기본 폼은 html에서 {{ form.as_p }}
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sub_title'] = '작성'
        context['btn_name'] = '생성'
        return context

        # test_dict ={
        #     'a': 1,
        #     'b': 2,
        #     'c': 3
        # }

     #    self.test(a=test_dict['a'], b=test_dict['b'], c=test_dict['c'])
     #    self.test(**test_dict)
     #
     #    test_list = [1,2,3]
     #    self.test(test_list[0], test_list[1], test_list[2])
     #    self.test(*test_list)
     #
     #
     # def test(self, a, b, c):
     #     return

class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    template_name = 'blog_form.html'
    #fields = ('category', 'title', 'content')
    form_class = BlogForm

    # 방법1. 404 오류, 작성자 본인만 수정 가능
    def get_queryset(self):
        queryset = super().get_queryset()

        # 관리자면 전체 글 조회
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(author=self.request.user)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sub_title'] = '수정'
        context['btn_name'] = '수정'
        return context

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

# 댓글 작성 처리 뷰
# BlogDetailView 클래스 post comment 주석 처리
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment # 댓글 모델로 동작하는 뷰
    form_class = CommentForm # 사용할 폼 클래스 설정

    def get(self, *args, **kwargs):
        raise Http404

    def form_valid(self, form):
        blog = self.get_blog()
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.blog = blog
        self.object.save()
        return HttpResponseRedirect(reverse('blog:detail', kwargs={'blog_pk':blog.pk}))

    # URL의 pk로 블로그 글을 가져오는 메서드
    def get_blog(self):
        pk = self.kwargs['blog_pk'] # comment pk랑 헷갈림 방지
        blog = get_object_or_404(Blog, pk=pk)
        return blog

# /comment/create/<int:blog_pk>/






