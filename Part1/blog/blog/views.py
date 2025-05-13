from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from blog.forms import BlogForm
from blog.models import Blog
import logging

logger = logging.getLogger(__name__)

#request 객체를 담는다.
def blog_list(request):
    # 모든 블로그 글을 생성일 기준 내림차순으로 가져옴
    blogs = Blog.objects.all().order_by('-created_at')

    # 검색어(q)를 GET 요청에서 받아옴 (예: ?q=검색어)
    q = request.GET.get('q')
    if q:
        # 검색할 기준
        blogs = blogs.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q)
        )

    # 블로그 글 목록을 10개씩 나눠서 페이지네이션 처리
    paginator = Paginator(blogs, 10)

    # GET 요청에서 현재 페이지 번호를 가져옴 (예: ?page=2)
    page = request.GET.get('page')

    # 해당 페이지 번호에 맞는 블로그 글 목록을 가져옴
    # 잘못된 값이 들어와도 자동으로 1페이지로 처리됨
    page_object = paginator.get_page(page)


    # 쿠키에서 'visits' 키로 저장된 값이 있으면 가져오고, 없으면 0
    # 쿠키는 문자열이므로 int로 변환 후 +1 (방문자 수 증가)
    visits = int(request.COOKIES.get('visits', 0)) + 1
    logger.info(f"현재 방문 횟수: {visits}")

    # 로거 보다는 ㅌ메플릿에서 값 추출이 더 직관적
    request.session['count'] = request.session.get('count', 0) + 1
    #request.session.modified = True  # 세션 수정 표시
    # # 세션 내용 출력
    # print("세션 내용:", request.session.items())

    context = {
        #'blogs':blogs,
        'object_list':page_object.object_list,
        'page_obj': page_object,
        'count': request.session['count']
    }
    #return render(request, 'blog_list.html', context)

    # HTML 렌더링
    response = render(request, 'blog_list.html', context)

    # visits 값을 쿠키로 다시 저장 (브라우저에 저장됨)
    response.set_cookie('visits', visits)

    # 최종적으로 사용자에게 응답 반환
    return response

def blog_detail(request, pk):
    # 없는 pk로 접속하면 오류남.
    #blog = Blog.objects.get(pk=pk)
    blog = get_object_or_404(Blog, pk=pk)
    context = {
        'blog':blog
    }
    return render(request, 'blog_detail.html', context)

@login_required()
def blog_create(request):
    # if not request.user.is_authenticated:
    #     return redirect(reverse('login'))
    form = BlogForm(request.POST or None)
    if form.is_valid():
        blog = form.save(commit=False)
        blog.author = request.user
        blog.save()
        return redirect(reverse('fb:detail', kwargs={'pk' : blog.pk}))

    context = {'form':form}
    return render(request, 'blog_form.html', context)

@login_required()
def blog_update(request, pk):
    if request.user.is_superuser:
        blog= get_object_or_404(Blog, pk=pk)
    else:
        blog = get_object_or_404(Blog, pk=pk, author=request.user)

    # pk와 작성자(author)가 현재 로그인한 사용자(request.user)인 Blog 객체를 조회
    # 조건에 맞는 객체가 없으면 404 에러 발생
    #blog = get_object_or_404(Blog, pk=pk, author=request.user)

    # BlogForm에 요청된 데이터(request.POST)를 넣고,
    # instance=blog로 기존 데이터를 불러와 폼을 채운다 (GET이면 기존 내용 표시, POST면 수정 데이터 반영)
    form = BlogForm(request.POST or None, request.FILES or None, instance=blog)
    print(request.POST)
    if form.is_valid():
        print(form.cleaned_data, request.FILES)
        blog.save()
        return redirect(reverse('fb:detail', kwargs={'pk': blog.pk}))

    context = {
        'form':form
    }
    return render(request, 'blog_form.html', context)
    # if request.user != blog.author:
    #     raise Http404

@login_required()
@require_http_methods(['POST']) # 특정 게시물(1/delete) 접속하여 삭제 시 405 에러
def blog_delete(request, pk):
    # if request.method != 'POST':
    #     raise Http4 04

    blog = get_object_or_404(Blog, pk=pk, author=request.user)
    blog.delete()

    return redirect(reverse('fb:list'))