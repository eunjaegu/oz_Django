from django.contrib.auth import get_user_model, login
from django.core import signing
from django.core.signing import TimestampSigner, SignatureExpired
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import FormView, DetailView

from config import settings
from member.forms import SignupForm, LoginForm
from member.models import UserFollowing
from utils.email import send_email

User = get_user_model()

# 회원가입
class SignupView(FormView):
    template_name = 'auth/signup.html'
    form_class = SignupForm
    #success_url = reverse_lazy('signup_done')

    def form_valid(self, form):
        user = form.save()  # 폼 데이터를 저장하여 user 객체 생성 (회원가입 처리)

        # 이메일 발송 준비
        # TimestampSigner : 특정 정보를 서명(암호화)하고, 나중에 검증할 수 있도록 해주는 도구
        signer = TimestampSigner()

        signed_user_email = signer.sign(user.email)  # 사용자 이메일에 서명을 추가하여 변조 방지
        signer_dump = signing.dumps(signed_user_email)  # 서명된 이메일을 직렬화해서 문자열로 변환 (URL 등에 넣기 위함)
        #signing.dumps()는 파이썬 객체를 직렬화(serialize) 해서, 문자열 형태로 만들어 주는 함수예요.

        # print(signer_dump)  # 디버깅: 직렬화된 서명 이메일 출력

        # 아래는 확인용 디코딩 과정 (실제 사용 안함, 디버깅용)
        # decoded_user_email = signing.loads(signer_dump)  # 직렬화된 문자열을 다시 파싱
        # print(decoded_user_email)  # 파싱된 결과 출력
        # email = signer.unsign(decoded_user_email, max_age=60 * 30)  # 최대 30분까지 유효한 서명을 원래 이메일로 복원
        # print(email)  # 복원된 이메일 출력

        # 이메일 인증 링크 생성
        # 예: http://localhost:8000/verify/?code=asdasdsa 처럼 생성됨
        url = f'{self.request.scheme}://{self.request.META["HTTP_HOST"]}/verify/?code={signer_dump}'
        if settings.DEBUG:
            print(url) # 생성된 인증 링크 출력 (실제로는 이메일로 보낼 예정)
        else:
            subject = '[Pystagram]이메일 인증을 완료해주세요.'  # 이메일 제목 설정
            message = f'다음 링클를 클릭해주세요. <br><a href="{url}">{url}</a>'   # 이메일 본문 (HTML 형식으로 링크 포함)

        send_email(subject, message, user.email)
        # 위에서 정의한 send_email 함수를 호출해 이메일 전송

        # 성공 페이지로 리다이렉트하는 대신 템플릿 렌더링으로 처리 (회원가입 완료 화면 표시)
        #return HttpResponseRedirect(self.get_success_url())
        return render(self.request, template_name='auth/signup_done.html', context ={'user': user})


def verify_email(request):
    # 1. 이메일 인증 링크에서 code 값을 추출 (예: /verify/?code=abc123)
    code = request.GET.get('code', '')

    # 2. TimestampSigner 인스턴스 생성 (서명/검증용)
    signer = TimestampSigner()

    try:
        # 3. 직렬화된 문자열을 복원
        decoded_user_email = signing.loads(code)

        # 4. 서명 검증 및 복호화 - 30분 유효 시간 설정
        email = signer.unsign(decoded_user_email, max_age=60 * 30)

    except (TypeError, SignatureExpired):
        # 5. 서명이 틀렸거나 만료, 변조된 경우 인증 실패 페이지 렌더링
        return render(request, template_name='auth/not_verified.html')

    # 6. 인증된 이메일로 비활성 사용자 조회
    user = get_object_or_404(User, email=email, is_active=False)

    # 7. 사용자 활성화 처리
    user.is_active = True
    user.save()

    # 8. 인증 완료 페이지 렌더링
    return redirect(reverse('login'))
    #return render(request, template_name='auth/email_verified_done.html', context={'user': user})

class LoginView(FormView):
    template_name = 'auth/login.html'
    form_class =  LoginForm
    success_url = reverse_lazy('main')

    # forms.py LoginForm 클래스의 clean 함수 통과
    # user가 인증과 활성화 되었는지 확인
    def form_valid(self, form):
        #email = form.cleaned_data['email']
        #user = User.objects.get(email=email)
        user = form.user
        login(self.request, user)   # 유저 받아서 로그인
        print(f'login {user.email}')

        # 로그인 후 이동할 '다음 페이지(next)' 파라미터를 URL에서 가져옴
        next_page = self.request.GET.get('next')
        # 만약 'next' 파라미터가 존재하면, 해당 페이지로 리다이렉트함
        if next_page:
            return HttpResponseRedirect(next_page)

        return HttpResponseRedirect(self.get_success_url())

# 닉네임으로 프로필 조회
class UserProfileView(DetailView):
    model = User
    template_name='profile/detail.html'

    # 기본적으로 DetailView는 pk로 객체를 찾지만, 아래 설정을 통해 'nickname'으로 찾도록 변경
    slug_field = 'nickname'     # User 모델에서 닉네임 필드(컬럼)를 slug로 사용
    slug_url_kwarg = 'slug'     # URLConf에서 <str:slug>로 전달된 값을 slug로 사용

    #prefetch_related('post_set', 'post_set__images') : user가 작성한 게시글, 게시글에 연결된 이미지 한번에 미리 가져온다.
    queryset = User.objects.all().prefetch_related('post_set', 'post_set__images', 'following', 'followers')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            data['is_follow'] = UserFollowing.objects.filter(
                to_user=self.object,
                from_user=self.request.user
            )

        return data

class UserFollowingView(View):
    def post(self, *args, **kwargs):
        pk = kwargs.get('pk', 0)
        to_user = get_object_or_404(User, pk=pk)

        # 나 자신 팔로우 시 에러
        if to_user == self.request.user:
            raise Http404

        # 만약 이미 팔로우가 되어 있으면  팔로우 취소 => UserFollowing row 삭제
        # 안되어 있으면 팔로우 시작 => UserFollowing row 생성
        following, created = UserFollowing.objects.get_or_create(
            to_user=to_user,
            from_user=self.request.user
        )
        if not created:
            following.delete()

        return HttpResponseRedirect(reverse('profile:detail', kwargs={'slug': to_user.nickname}))






