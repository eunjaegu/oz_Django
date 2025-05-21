from urllib.parse import urlencode, parse_qs

import requests
from django.conf import settings
from django.contrib.auth import login, get_user_model
from django.core import signing
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views.generic import RedirectView


from member.forms import NicknameForm

User = get_user_model()

# 네이버 API 관련 상수 정의
NAVER_CALLBACK_URL = '/oauth/naver/callback/'
NAVER_STATE = 'naver_login' # CSRF 방지를 위한 state 값
NAVER_LOGIN_URL = 'https://nid.naver.com/oauth2.0/authorize' # 네이버 로그인 인증 요청, 출력:URL 리다이렉트
NAVER_TOKEN_URL = 'https://nid.naver.com/oauth2.0/token'     # 접근 토큰 발급/갱신/삭제 요청, 출력:json
NAVER_PROFILE_URL = 'https://openapi.naver.com/v1/nid/me'    # 네이버 회원 프로필 조회, 출력:json

# 깃허브 API 관련 상수 정의
GITHUB_CALLBACK_URL = '/oauth/github/callback/'
GITHUB_STATE = 'github_login' # CSRF 방지를 위한 state 값
GITHUB_LOGIN_URL = 'https://github.com/login/oauth/authorize'
GITHUB_TOKEN_URL = 'https://github.com/login/oauth/access_token'
GITHUB_PROFILE_URL = 'https://api.github.com/user'


# 1단계: 사용자가 "네이버 로그인" 버튼 클릭 시 → 네이버 로그인 페이지로 이동
class NaverLoginRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        domain = self.request.scheme + '://' + self.request.META.get('HTTP_HOST', '')
        callback_url = domain + NAVER_CALLBACK_URL  # 인증 후 다시 돌아올 URL

        state = signing.dumps(NAVER_STATE)  # CSRF 방지용 state를 암호화
        print(state)

        # 네이버 로그인 URL에 보낼 파라미터
        params = {
            'response_type': 'code',  # 기본값, 인증 과정에 대한 내부 구분값으로 'code'로 전송해야 함 -> 그래야지 인증 url인지 알아
            'client_id': settings.NAVER_CLIENT_ID,  # 네이버 앱 클라이언트 ID
            'redirect_uri': callback_url,  # 인증 완료 후 리다이렉트 주소
            'state': state  # CSRF 방지를 위한 값
        }

        # 2단계: Django → 네이버 (로그인 요청 URL로 리다이렉트)
        #print(f'{NAVER_LOGIN_URL}?{urlencode(params)}')
        return f'{NAVER_LOGIN_URL}?{urlencode(params)}'

# 3~7단계: 콜백에서 토큰 받고 사용자 정보 받아 로그인 처리
def naver_callback(request):
    code = request.GET.get('code')  # 코드 : access token 발급을 위한 열쇠
    state = request.GET.get('state')

    # 3단계: 네이버 → Django (code, state 반환)
    # 4단계: CSRF 방지용 state 값 검증  # NAVER_STATE = naver_login
    if NAVER_STATE != signing.loads(state):
        raise Http404
    # 5단계: Django → 네이버 권한 서버 (access token 요청)
    # 아래 get_naver_access_token 함수 참조
    access_token = get_naver_access_token(code, state)

    # 6단계: Django → 네이버 OpenAPI (사용자 정보 요청)
    # 아래 def get_naver_profile 함수 참조
    profile_response = get_naver_profile(access_token)

    print('profile request', profile_response)
    # 7단계: 네이버 OpenAPI → Django (사용자 정보 응답)
    email = profile_response.get('email')
    print(email)

    # 8단계: 사용자 email로 가입 여부 확인 후 로그인 처리
    user = User.objects.filter(email=email).first()

    if user:
        if not user.is_active:
            user.is_active = True
            user.save()

        login(request, user)
        return redirect('main')
    return redirect(reverse('oauth:nickname') + f'?access_token={access_token}&oauth=naver')

class GithubLoginRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        domain = self.request.scheme + '://' + self.request.META.get('HTTP_HOST', '')
        callback_url = domain + GITHUB_CALLBACK_URL  # 인증 후 다시 돌아올 URL

        state = signing.dumps(GITHUB_STATE)  # CSRF 방지용 state를 암호화
        print(state)

        # 네이버 로그인 URL에 보낼 파라미터
        params = {
            'response_type': 'code',  # 기본값, 인증 과정에 대한 내부 구분값으로 'code'로 전송해야 함 -> 그래야지 인증 url인지 알아
            'client_id': settings.GITHUB_CLIENT_ID,  # 네이버 앱 클라이언트 ID
            'redirect_uri': callback_url,  # 인증 완료 후 리다이렉트 주소
            'state': state  # CSRF 방지를 위한 값
        }

        # 2단계: Django → 네이버 (로그인 요청 URL로 리다이렉트)
        print(f'{GITHUB_LOGIN_URL}?{urlencode(params)}')
        return f'{GITHUB_LOGIN_URL}?{urlencode(params)}'

def github_callback(request):
    code = request.GET.get('code')  # 코드 : access token 발급을 위한 열쇠
    state = request.GET.get('state')

    if GITHUB_STATE != signing.loads(state):
        raise Http404
    print(state)

    access_token = get_github_access_token(code, state)
    if not access_token:
        raise Http404

    profile_response = get_github_profile(access_token)

    print('profile request', profile_response)
    email = profile_response.get('email')
    print(email)

    user = User.objects.filter(email=email).first()

    if user:
        if not user.is_active:
            user.is_active = True
            user.save()

        login(request, user)
        return redirect('main')
    return redirect(reverse('oauth:nickname') + f'?access_token={access_token}&oauth=github' )
# 닉네임 설정
def oauth_nickname(request):
    access_token = request.GET.get('access_token')
    oauth = request.GET.get('oauth')

    if not access_token or oauth not in ['naver', 'github']:
        return redirect('login')

    form = NicknameForm(request.POST or None)

    #닉네임 유효성 검사
    if form.is_valid():
        # 임시저장
        user = form.save(commit=False)

        # 토큰으로 네이버 사용자 프로필을 가져온다.
        if oauth == 'naver':
            profile = get_naver_profile(access_token)
        else:
            profile = get_github_profile(access_token)

        email = profile.get('email')    # 프로필에서 이메일 추출한다.

        # 같은 이메일을 가진 사용자가 있다면 404에러 발생(중복 가입 방지)
        if User.objects.filter(email=email).exists():
              raise Http404

        # 사용자 객체에 네이버 이메일을 할당
        user.email = email

        # 활성화로 만들기
        user.is_active = True
        # 무작위 비밀번호를 설정합니다 (비밀번호는 실제 사용자가 몰라도 됨)
        random_password = get_random_string(12)  # 12자리 랜덤 문자열 생성
        user.set_password(random_password)

        #user.set_password(User.objects.make_random_password())
        #random_pw = User.objects.make_random_password()
        #print(f'유저비밀번호 : {user.password}')

        # 실제로 DB에 저장
        user.save()

        #로그인 처리 (세션에 사용자 정보 저장)
        login(request, user)
        # 로그인 성공 시 메인페이지로 이동
        return redirect('main')
    #닉네임 폼을 다시 보여줍니다 (처음 접근했거나 폼 검증 실패 시)
    return render(request, 'auth/nickname.html', {'form':form})


def get_naver_access_token(code, state):
    # 5단계: Django → 네이버 권한 서버 (access token 요청)
    params = {
        'grant_type': 'authorization_code',
        'client_id': settings.NAVER_CLIENT_ID,
        'client_secret': settings.NAVER_SECRET,
        'code': code,
        'state': state
    }

    # 네이버에 access token 발급 요청을 보내고, 응답(JSON)을 파싱함
    response = requests.get(NAVER_TOKEN_URL, params=params)
    result = response.json() #JSON 문자열을 Python 딕셔너리로 변환하는 것

    # 네이버에 보낸 json 응답을 결과에 담아 조회해서 access_token을 추출
    return result.get('access_token')

def get_naver_profile(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(NAVER_PROFILE_URL, headers=headers)

    if response.status_code != 200:
        raise Http404

    result = response.json()
    return result.get('response')

def get_github_access_token(code, state):
    # 5단계: Django → 네이버 권한 서버 (access token 요청)
    params = {
        #'grant_type': 'authorization_code',
        'client_id': settings.GITHUB_CLIENT_ID,
        'client_secret': settings.GITHUB_SECRET,
        'code': code,
        'state': state,
        #'redirect_uri': settings.GITHUB_REDIRECT_URI
    }

    print("✅ Access Token 요청 전체 data:", params)

    response = requests.get(GITHUB_TOKEN_URL, params=params)
    response_str = response.content.decode()

    response_dict = parse_qs(response_str)
    access_token = response_dict.get('access_token', [])[0]
    print(f"'응답내용:' {response.content}")
    return access_token

def get_github_profile(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(GITHUB_PROFILE_URL, headers=headers)
    print(f"'사용자 정보:' {response.content}")

    if response.status_code != 200:
        raise Http404

    result = response.json()

    if not result.get('email'):
        result['email'] = f'{result["login"]}@id.github.com'

    print('*'*100)
    print(result)
    print('*'*100)
    return result





