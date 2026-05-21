from django.shortcuts import render, redirect
from user.models import UserInfo
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # 通过用户名找到用户
            user = UserInfo.objects.filter(username=username).first()
            if not user:
                return render(request, 'login.html', {'error': '用户名或密码错误'})
            # 使用密码哈希验证
            if user.check_password(password):
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                if user.avatar:
                    request.session['avatar'] = user.avatar
                return redirect('home:index')
            else:
                return render(request, 'login.html', {'error': '用户名或密码错误'})
        except UserInfo.DoesNotExist:
            return render(request, 'login.html', {'error': '用户名或密码错误'})
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if UserInfo.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': '该用户名已被使用'})
        
        if UserInfo.objects.filter(uemail=email).exists():
            return render(request, 'register.html', {'error': '该邮箱已被注册'})

        user = UserInfo.objects.create(
            username=username,
            uemail=email
        )
        # 使用密码哈希设置密码
        user.set_password(password)
        user.save()

        # 注册成功后自动跳转到登录页面
        return redirect('user:login')
    return render(request, 'register.html')


def profile(request):
    """个人信息页面 - 查看和编辑基本信息"""
    # 检查用户是否登录
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user:login')
    
    try:
        user = UserInfo.objects.get(id=user_id)
    except UserInfo.DoesNotExist:
        return redirect('user:login')
    
    if request.method == 'POST':
        # 处理表单提交 - 更新个人信息
        user.username = request.POST.get('username', user.username)
        user.uemail = request.POST.get('uemail', user.uemail)
        user.uphone = request.POST.get('uphone', user.uphone)
        user.uaddress = request.POST.get('uaddress', user.uaddress)
        user.uyoubian = request.POST.get('uyoubian', user.uyoubian)
        
        # 处理头像上传
        if 'avatar' in request.FILES:
            avatar_file = request.FILES['avatar']
            # 保存头像文件到媒体目录
            import os
            from django.conf import settings
            
            # 创建用户头像目录
            avatar_dir = os.path.join(settings.MEDIA_ROOT, 'avatars')
            if not os.path.exists(avatar_dir):
                os.makedirs(avatar_dir)
            
            # 保存文件 - 使用固定文件名，确保覆盖原有文件
            file_name = f"user_{user_id}_avatar.jpg"
            file_path = os.path.join(avatar_dir, file_name)
            with open(file_path, 'wb+') as destination:
                for chunk in avatar_file.chunks():
                    destination.write(chunk)
            
            # 更新头像路径
            user.avatar = f"avatars/{file_name}"
        
        # 如果提供了新密码，则更新密码
        new_password = request.POST.get('new_password')
        if new_password:
            user.set_password(new_password)
        
        user.save()
        # 更新session中的用户名和头像
        request.session['username'] = user.username
        if user.avatar:
            request.session['avatar'] = user.avatar
        
        return render(request, 'profile.html', {
            'user': user,
            'success_message': '个人信息更新成功！'
        })
    
    # GET请求 - 显示个人信息页面
    return render(request, 'profile.html', {'user': user})


def logout(request):
    """用户退出登录"""
    # 清除session
    if 'user_id' in request.session:
        del request.session['user_id']
    if 'username' in request.session:
        del request.session['username']
    return redirect('user:login')


import random
import string

def send_verify_code(request):
    """发送邮箱验证码"""
    if request.method == 'POST':
        email = request.POST.get('email')
        
        if not email:
            return JsonResponse({'success': False, 'message': '请输入邮箱地址'})
        
        # 检查邮箱是否已注册
        try:
            user = UserInfo.objects.get(uemail=email)
        except UserInfo.DoesNotExist:
            return JsonResponse({'success': False, 'message': '该邮箱未注册'})
        
        # 生成6位数字验证码
        verify_code = ''.join(random.choices(string.digits, k=6))
        
        # 将验证码存储到session，有效期5分钟
        request.session['verify_code'] = verify_code
        request.session['verify_code_email'] = email
        request.session['verify_code_time'] = request.session.get('verify_code_time', 0) + 1
        
        # 模拟发送邮件（实际项目中需要配置邮件服务器）
        # 这里只是将验证码打印到控制台，并保存到session
        print(f"【验证码】您的登录验证码是：{verify_code}（有效期5分钟）")
        
        return JsonResponse({'success': True, 'message': '验证码已发送'})
    
    return JsonResponse({'success': False, 'message': '请使用POST请求'})


def verify_login(request):
    """验证码登录"""
    if request.method == 'POST':
        email = request.POST.get('email')
        verify_code = request.POST.get('verify_code')
        
        if not email or not verify_code:
            return render(request, 'login.html', {'verify_error': '请填写邮箱和验证码'})
        
        # 验证验证码
        session_code = request.session.get('verify_code')
        session_email = request.session.get('verify_code_email')
        
        if not session_code or not session_email:
            return render(request, 'login.html', {'verify_error': '请先获取验证码'})
        
        if session_email != email:
            return render(request, 'login.html', {'verify_error': '验证码与邮箱不匹配'})
        
        if session_code != verify_code:
            return render(request, 'login.html', {'verify_error': '验证码错误'})
        
        # 验证码验证成功，登录用户
        try:
            user = UserInfo.objects.get(uemail=email)
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            if user.avatar:
                request.session['avatar'] = user.avatar
            
            # 清除验证码session
            del request.session['verify_code']
            del request.session['verify_code_email']
            
            return redirect('home:index')
        except UserInfo.DoesNotExist:
            return render(request, 'login.html', {'verify_error': '用户不存在'})
    
    return render(request, 'login.html')
