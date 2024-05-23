import os
import django
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
fake = Faker()

def create_fake_users(n):
    for _ in range(n):
        email = fake.email()
        username = email.split('@')[0]
        first_name = fake.first_name()
        last_name = fake.last_name()
        nickname = fake.user_name()
        password = '1111'  # 임의의 비밀번호 설정, 실제 환경에서는 보안에 유의해야 합니다.

        user = User.objects.create_user(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            nickname=nickname,
            password=password
        )
        user.save()
        print(f'{username} created')

# 50명의 사용자 생성
create_fake_users(50)
