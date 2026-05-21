import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel.settings')
django.setup()

from user.models import UserInfo

test_user, created = UserInfo.objects.get_or_create(
    uemail='test@example.com',
    defaults={
        'username': 'testuser',
        'password': '123456'
    }
)

if created:
    print(f'测试用户创建成功！')
    print(f'邮箱: test@example.com')
    print(f'密码: 123456')
else:
    print(f'测试用户已存在！')
    print(f'邮箱: test@example.com')
    print(f'密码: 123456')
