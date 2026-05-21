from django.contrib import admin
from sqlalchemy.testing.pickleable import User
from django.utils.html import format_html
from user.models import UserInfo

# 修改Django管理后台的显示名称
admin.site.site_header = "旅游管理系统"  # 页面顶部显示
admin.site.site_title = "旅游管理"       # 浏览器标签页显示
admin.site.index_title = "后台管理"      # 首页标题


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'uemail','uphone','uaddress','created_at','show_avatar')
    #可以进入编辑页面的字段
    list_display_links = ('username','uemail')
    #可筛选字段
    list_filter =('created_at',)
    search_fields = ('username','uemail','uphone')
    #分页设置
    list_per_page=20
    #按创建时间排序(默认排序)
    ordering=('-created_at',)
    #编辑页面的字段分组
    fieldsets=(
    ('基本信息',{'fields':('username','password','uemail','avatar')}),
    (
        '联系信息',{'fields':('uphone','uaddress','uyoubian')}
    ),
    ('其他信息',{'fields':('created_at',)}
    )
    )
    #自定义头像显示
    def show_avatar(self,obj):
        if obj.avatar:
            # avatar字段是CharField，存储的是相对路径
            return format_html(
                '<img src="/media/{}" style="max-height:50px; max-width:50px; border-radius:50px;" />',
                obj.avatar)
        return format_html('<span style="color:gray;">无头像</span>')

    show_avatar.short_description='头像预览'
    show_avatar.admin_order_field='avatar'


#注册模型和对应的admin类
admin.site.register(UserInfo,UserAdmin)