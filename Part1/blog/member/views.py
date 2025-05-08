from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login as django_login
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import logout as django_logout


# 회원가입 폼을 화면에 출력(렌더링)
def sign_up(request):
    #POST 요청 시에만 의미가 있고, GET 요청 시 에러방지를 위해 .get을 사용하여 None 반환
    # username = request.POST.get('username')
    # password1 = request.POST.get('password1')
    # password2 = request.POST.get('password2')
    #
    # print('username', username)
    # print('password1', password1)
    # print('password2', password2)

    # username 중복확인작업
    # 패스워드가 맞는지, 그리고 패스워드 정책에 올바른지 (대소문자)

    form = UserCreationForm(request.POST or None)
    if form.is_valid():  # 값이 있으면 저장
        form.save()
        return redirect(settings.LOGIN_URL)

    # if request.method == 'POST':
    #     # UserCreationForm은 models과 연관이 있어 save하면 user가 등록됨.
    #     form = UserCreationForm(request.POST)
    #     if form.is_valid(): # 값이 있으면 저장
    #         form.save()
    #         return redirect('/accounts/login/')
    # else: # GET 요청일 때만 새 폼 생성
    #     form = UserCreationForm()

    context = {
        'form': form
    }
    return render(request, 'registration/signup.html', context)


def login(request):
    form = AuthenticationForm(request, request.POST or None)
    if form.is_valid():
        # 아이디와 비밀번호 일치 시 User객체 세션에 등록
        django_login(request, form.get_user())

        next = request.GET.get('next')
        if next:
            return redirect(next)

        print("로그인후 후 세션:", request.session.items())

        return redirect(reverse('blog:list'))
    else:
        form = AuthenticationForm(request)

    context = {
        'form': form
    }

    return render(request, 'registration/login.html', context)
