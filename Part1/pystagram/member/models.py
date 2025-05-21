from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

from utils.models import TimestampModel

# BaseUserManager : 기능 구현(사용자 객체를 생성하는 로직)
# 사용자 생성을 위한 커스텀 매니저 클래스
class UserManager(BaseUserManager):
    # 일반 사용자 생성 메서드
    def create_user(self, email, password):
        if not email:
            raise ValueError('올바른 이메일을 입력하세요.')

        # self.model은 아래 정의된 User 모델(클래스)을 참조함
        user = self.model(
            email=self.normalize_email(email)   #이메일 정규화 처리
        )
        user.set_password(password) # 비밀번호 해시화 저장
        user.is_active = False     # 기본적으로 비활성 상태 (이메일 인증 등 필요 시 사용)
        user.save(using=self._db)                 # DB 저장 (_db는 다중 DB 사용 시 지정 가능)
        return user

    # superuser 생성 명령어 실행 시 호출됨: python manage.py createsuperuser
    def create_superuser(self, email, password):
        user=self.create_user(email, password)
        user.is_admin = True
        user.is_active = True   # 관리자 계정은 바로 활성화
        user.save(using=self._db)
        return user

# 암호화 qwer1234 -> asdasdzsdf343 -> 복호화 -> qwer1234
# 해시화 qwer1234 -> asdas / dzsdf343 -> 암호화(asdas) -> 암호화를 반복 -> aqldkfjlda -> 복호화 불가능

# AbstractBaseUser :기본 테이블 (모델구조)
# 장고 기본 User 모델은 `username`을 기본 인증 필드로 사용하지만,
# `AbstractBaseUser`를 상속받아 커스텀 User 모델을 정의하여,
# 이메일(`email`)을 사용자 인증 필드로 사용하도록 수정
# 이를 통해 `username` 대신 이메일을 사용하여 로그인 및 인증을 처리
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email',
        unique=True # 중복 불가 (로그인 ID로 사용)
    )
    is_active = models.BooleanField(default=False)  #계정 활성화 여부
    is_admin = models.BooleanField(default=False)   #관리자 권한 부여
    nickname = models.CharField('nickname', max_length=20, unique=True)

    # 1. 팔로우(Follow) 관계 설명
    #    - 내가 팔로우하는 사람들 "팔로잉(following)": user.following.all()
    #    - 나를 팔로우하는 사람들 "팔로워(followers)": user.followers.all() ← related_name='followers' 덕분에 사용 가능

    # 2. 관계 구조
    #    - USER <-> USER: 다대다(ManyToMany) 관계

    # 3. 'self' 사용 이유
    #    - 같은 모델(USER) 간의 관계이므로 'self'로 지정 (자기 자신과의 관계 가능)

    # 4. symmetrical 설정
    #    - symmetrical=False (단방향: A => B)
    #      A가 B를 팔로우해도, B는 A를 자동으로 팔로우하지 않음(A(나)만 팔로우)
    #      예: A.following.add(B) → B는 A를 팔로우하지 않음 (SNS 팔로우 기능에 적합)
    #
    #    - symmetrical=True (양방향: A <=> B)
    #      A가 B를 팔로우하면, B도 A를 자동으로 팔로우한 것으로 간주됨
    #      예: A.friends.add(B) → B.friends에도 A가 자동 추가됨 (친구 기능에 적합)

    # 5. related_name 사용 이유
    #    - 역방향 참조를 위해 사용됨
    #    - 예:
    #    - A.following.all() → A가 팔로우한 사용자 목록
    #    - A.followers.all() → A를 팔로우하고 있는 사용자 목록

    # 6. through='UserFollowing'
    #  - ManyToMany 관계를 직접 연결하는 대신, 중간 모델인 'UserFollowing'을 통해 관계를 관리함
    #  - 단순 연결이 아니라 추가 정보(팔로우 날짜, 상태 등)를 저장하거나 팔로우 관계를 더 세밀하게 제어할 때 사용
    #  - 단순 연결만 필요하면 ManyToManyField만 사용하면 됨
    #  - 추가 정보를 다루려면 중간 모델을 정의하고 through 옵션에 지정함(지금처럼)

    # 7. through_fields=('from_user', 'to_user')
    # - 중간 모델 'UserFollowing'에서
    # - 'from_user' 필드는 팔로우를 하는 사람(출발지),
    # - 'to_user' 필드는 팔로우 당하는 사람(도착지)을 나타내며, 이 필드들이 ManyToMany 관계의 연결 방향을 명확히 지정함


    following = models.ManyToManyField(
        'self', symmetrical=False, related_name='followers',
        through='UserFollowing',    # 6.
        through_fields=('from_user', 'to_user') # 7.
    )


    objects = UserManager() # 앞서 정의한 UserManager를 설정

    USERNAME_FIELD = 'email'    #로그인 시 사용할 필드 지정
    EMAIL_FIELD = 'email'       #이메일 필드로 사용
    REQUIRED_FIELDS = []         # cr eatesuperuser 시 추가로 요구할 필드

    # 관리자(admin) 인터페이스 표시 설정
    class Meta:
        verbose_name = ('유저')                       #admin에서 단수
        verbose_name_plural = f'{verbose_name} 목록'  #admin에서 복수

    def get_full_name(self):
        return self.nickname    # 닉네임을 전체 이름으로 반환

    def get_short_name(self):
        return self.nickname    # 닉네임을 짧은 이름으로 반환

    def __str__(self):
        return self.nickname    # 객체 출력 시 닉네임으로 보이게 설정

    # 권한 관련 메서드: True로 반환하여 모든 권한을 허용
    def has_perm(self, perm, obj=None):
        return True # 모든 권한을 허용

    def has_module_perms(self, app_label):
        return True # 모든 모듈 권한을 허용

    # @property : 함수이며, 클래스 변수처럼 사용
    # user.is_superuser
    @property
    def is_staff(self):
        return self.is_admin    # is_staff가 True면 admin 사이트 접근 가능

    @property
    def is_superuser(self):
        return self.is_admin    # superuser 여부도 is_admin으로 판단


class UserFollowing(TimestampModel):
    # 친구 맺고 싶은 유저(다른 사람) / 다른 사람이 나를 팔로워
    to_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_followers')

    # 현재 로그인 된 유저(나) / 내가 팔로잉
    from_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_following')

    class Meta:
        unique_together = ('to_user', 'from_user')
    # to_user 1, from_user 2
    # to_user 1, from_user 3
    # to_user 1, from_user 4

    # to_user 1, from_user 2 => 오류








