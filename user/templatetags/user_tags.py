from django import template
from user.models import UserInfo
from django.conf import settings
import os

register = template.Library()

@register.simple_tag
def get_user_avatar(user_id):
    """获取用户头像路径，如果不存在则返回None"""
    try:
        user = UserInfo.objects.get(id=user_id)
        if user.avatar:
            # 检查头像文件是否存在
            avatar_path = os.path.join(settings.MEDIA_ROOT, user.avatar)
            if os.path.exists(avatar_path):
                return user.avatar
        return None
    except UserInfo.DoesNotExist:
        return None
