from django.utils.deprecation import MiddlewareMixin
from home.models import PageVisit
import re

# 定义页面名称映射
PAGE_NAME_MAP = {
    'home/index': '首页',
    'home/travel_list': '旅游景点列表',
    'home/rating_stats': '评分分布统计',
    'home/hot_spots': '热门景点排行',
    'home/price_analysis': '门票价格分析',
    'home/word_cloud': '景点信息词云',
    'home/region_distribution': '景点区域分布',
    'home/ai_chat': '旅游信息智能客服',
    'home/travel_route': 'AI旅游路线推荐',
    'home/generate_travel_route': '生成旅游路线',
    'user/profile': '个人信息管理',
    'user/login': '用户登录',
    'user/register': '用户注册',
    # 旧的URL路径映射（用于兼容历史数据）
    'home/part1': '评分分布统计',
    'home/part2': '热门景点排行',
    'home/part3': '门票价格分析',
    'home/part4': '景点信息词云',
    'home/part5': '景点区域分布',
}

class PageVisitMiddleware(MiddlewareMixin):
    """页面访问统计中间件"""
    
    def process_request(self, request):
        # 排除静态文件和admin页面
        path = request.path
        if path.startswith('/admin/') or path.startswith('/static/') or path.startswith('/media/'):
            return
        
        # 获取页面名称
        page_name = self.get_page_name(path)
        
        # 更新访问统计
        try:
            page_visit, created = PageVisit.objects.get_or_create(
                page_url=path,
                defaults={'page_name': page_name}
            )
            if created:
                page_visit.page_name = page_name
            page_visit.visit_count += 1
            page_visit.save()
        except Exception as e:
            # 避免中间件异常影响正常请求
            pass
    
    def get_page_name(self, path):
        """根据URL路径获取页面名称"""
        # 去掉末尾斜杠
        path = path.rstrip('/')
        
        # 检查是否在映射表中
        for key, name in PAGE_NAME_MAP.items():
            if path.endswith(key):
                return name
        
        # 如果不在映射表中，直接使用路径作为名称
        return path
