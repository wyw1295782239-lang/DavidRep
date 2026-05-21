from django.urls import path
from home import views
app_name='home'
urlpatterns = [
    path('',views.index,name='index'),
    path('index',views.index,name='index'),
    path('travel_list',views.travel_list,name='travel_list'),
    # 数据分析页面 - 新的英文命名
    path('rating_stats', views.rating_stats, name='rating_stats'),      # 评分统计
    path('hot_spots', views.hot_spots, name='hot_spots'),             # 热门景点排行
    path('price_analysis', views.price_analysis, name='price_analysis'), # 门票价格分析
    path('word_cloud', views.word_cloud, name='word_cloud'),          # 景点信息词云
    path('region_distribution', views.region_distribution, name='region_distribution'), # 区域分布
    # AI功能页面
    path('ai_chat',views.ai_chat,name='ai_chat'),
    path('generate_travel_route',views.generate_travel_route,name='generate_travel_route'),
    path('travel_route',views.generate_travel_route,name='travel_route'),
    # API接口
    path('submit_review',views.submit_review,name='submit_review'),
    # 后台管理统计页面
    path('user_stats', views.user_stats, name='user_stats'),  # 用户注册数统计

]
