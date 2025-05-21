from django.core.mail import send_mail

from config import settings

    # 이메일을 보내는 함수 정의
    # 매개변수:
    # subject : 이메일 제목
    # message : 이메일 본문 내용
    # to_email : 수신자 이메일 주소 (문자열 또는 리스트 가능)

def send_email(subject, message, to_email):
    to_email = to_email if isinstance(to_email, list) else [to_email]
    # to_email이 리스트인지 확인
    # → 리스트가 아니면, 리스트로 감싸서 리스트 형태로 변환
    # (send_mail 함수는 수신자 주소를 리스트로 받기 때문)

    # if isinstance(to_email, list):
    #     to_email = to_email
    # else:
    #     to_email = [to_email,]

    send_mail(subject, message, settings.EMAIL_HOST_USER, to_email)
    # Django의 send_mail 함수를 사용해 메일 전송
    # 매개변수:
    # - subject: 메일 제목
    # - message: 메일 본문
    # - settings.EMAIL_HOST_USER: 발신자 주소 (settings.py에 정의됨)
    # - to_email: 수신자 리스트

