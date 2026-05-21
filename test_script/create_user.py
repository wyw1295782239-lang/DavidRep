
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel.settings')
django.setup()

from user.models import UserInfo

try:
    test_user, created = UserInfo.objects.get_or_create(
        uemail='test@example.com',
        defaults={
            'username': 'testuser',
            'password': '123456'
        }
    )
    
    if created:
        print('测试用户创建成功！')
    else:
        print('测试用户已存在！')
    
    print('邮箱: test@example.com')
    print('密码: 123456')
except Exception as e:
    print(f'错误: {e}')
