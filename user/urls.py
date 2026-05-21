from django.urls import path
from user import views

app_name = 'user'

urlpatterns = [
    path('', views.login),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('profile', views.profile, name='profile'),
    path('logout', views.logout, name='logout'),
    path('send_verify_code', views.send_verify_code, name='send_verify_code'),
    path('verify_login', views.verify_login, name='verify_login'),
]