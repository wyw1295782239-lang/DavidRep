from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

class UserInfo(models.Model):
    username = models.CharField(max_length=20, verbose_name='用户名', unique=True)
    password = models.CharField(max_length=128,verbose_name='密码')
    uemail = models.CharField(max_length=40, verbose_name='邮箱', unique=True)
    uaddress = models.CharField(max_length=40,verbose_name='地址',default='')
    uyoubian = models.CharField(max_length=30,verbose_name='邮编',default='')
    uphone = models.CharField(max_length=30,verbose_name='手机号',default='')
    avatar = models.CharField(max_length=255,verbose_name='头像',default='')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def set_password(self, raw_password):
        """设置密码，使用Django的密码哈希"""
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        """验证密码"""
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username

    #后台管理页面显示
    class Meta:
        verbose_name_plural = '用户管理'