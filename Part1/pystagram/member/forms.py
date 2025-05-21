from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm

from utils.forms import BootstrapModelForm

# Auth_user_model(config/settings.py -> member.User) or 기본_유저_모델(없으면)
User = get_user_model()

class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # class_default_fields = ('password1', 'password2')

        for field in ('password1', 'password2'):
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['placeholder'] = 'password'
            if field == 'password1':
                self.fields[field].label = '비밀번호'
            else:
                self.fields[field].label = '비밀번호 확인'

    class Meta(UserCreationForm):
        model = User
        fields = ('email', 'nickname', )
        labels = {
            'email': '이메일',
            'nickname': '닉네임',
        }
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'example@example.com',
                    'class':'form-control',

                }
            ), 'nickname': forms.TextInput(
                attrs={
                    'placeholder': '닉네임',
                    'class': 'form-control',
                }
            )
        }

class LoginForm(forms.Form):
    email = forms.CharField(
        label='이메일',
        required=True,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'example@example.com',
                'class' : 'form-control'
            }
        )
    )
    password = forms.CharField(
        label='패스워드',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'password',
                'class': 'form-control'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    # form.cleaned_data
    # 사용자가 폼(form)에 입력한 데이터를 유효성 검사(validation) 한 후,
    # 유효한 값만 모아둔 딕셔너리(dictionary) 형태입니다.
    def clean(self):
        cleaned_data=super().clean()            # 부모 클래스의 clean() 호출해 기본 검증 및 cleaned_data를 받음
        email=cleaned_data.get('email')         # 폼에서 검증된 email 값 가져오기
        password=cleaned_data.get('password')   # 폼에서 검증된 password 값 가져오기

        # Django 인증 함수로 사용자 인증 시도
        self.user=authenticate(email=email, password=password)

        if not self.user:
            raise forms.ValidationError('이메일 또는 패스워드가 올바르지 않습니다.')

        if not self.user.is_active:
            # 인증 실패 시 에러 발생
            raise forms.ValidationError('유저가 인증되지 않았습니다.')
        # 최종적으로 검증된 데이터 리턴
        return cleaned_data

class NicknameForm(BootstrapModelForm):
    class Meta:
        model = User
        fields = ('nickname', )
        labels = {
            'nickname': '닉네임을 입력하여 회원가입을 완료해주세요.'
        }


