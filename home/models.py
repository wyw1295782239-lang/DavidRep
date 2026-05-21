import uuid
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class TravelInfo(models.Model):
        unique_id = models.BigIntegerField(null=True,verbose_name='唯一标识')
        area = models.CharField(max_length=255,null = True,verbose_name='所在区域')
        name = models.CharField(max_length=255,null=True,verbose_name='景点名称')
        review_count = models.IntegerField(null=True,verbose_name='评论数量')
        rating = models.CharField(max_length=50,null=True,verbose_name='评分')
        is_ad =models.BooleanField(default=False,null=True,verbose_name='是否为广告')
        is_recommended = models.BooleanField(default=False,null=True,verbose_name='是否被推荐')
        city = models.CharField(max_length=50,null=True,verbose_name='城市名称')
        image_url =models.CharField(max_length=500,null=True,verbose_name='图片链接')
        distance_from_center = models.CharField(max_length=255,null=True,verbose_name='与市中心的距离')
        tags = models.CharField(max_length=255,null=True,verbose_name='标签')
        detail_link=models.CharField(max_length=500,null=True,verbose_name='详情页链接')
        market_price =models.CharField(null=True,verbose_name='市场售价',max_length=255)
        discount_price = models.CharField(null=True,verbose_name='优惠价格',max_length=255)
        discount_description = models.CharField(max_length=255,null=True,verbose_name='优惠描述')
        actual_price = models.CharField(null=True,verbose_name='实际票价',max_length=255)
        price_type = models.CharField(null=True,verbose_name='价格类型',max_length=255)
        price_type_description = models.CharField(max_length=100,null=True,verbose_name='价格类型描述')
        is_free = models.BooleanField(default=False,null=True,verbose_name='是否免费')
        longitude=models.FloatField(null=True,verbose_name='经度')
        latitude = models.FloatField(null=True,verbose_name='纬度')
        popularity_score = models.CharField(null=True,verbose_name='热度评分',max_length=255)
        province=models.CharField(max_length=100,null=True,verbose_name='省份')
        
        def __str__(self):
            return self.name or f'TravelInfo {self.pk}'

class TravelRoute(models.Model):
    """旅游路线"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='用户')
    city = models.CharField(max_length=100, verbose_name='目的地')
    season = models.CharField(max_length=20, verbose_name='季节')
    days = models.IntegerField(verbose_name='行程天数')
    budget = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='总预算')
    table_content = models.TextField(verbose_name='路线表格内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '旅游路线'
        verbose_name_plural = '旅游路线管理'

class RoutePoint(models.Model):
    """路线景点"""
    route = models.ForeignKey(TravelRoute, on_delete=models.CASCADE, verbose_name='旅游路线')
    name = models.CharField(max_length=255, verbose_name='景点名称')
    visit_time = models.CharField(max_length=100, verbose_name='游玩时间')
    feature = models.TextField(verbose_name='景色特点')
    longitude = models.FloatField(verbose_name='经度')
    latitude = models.FloatField(verbose_name='纬度')
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='预计花费')
    order = models.IntegerField(verbose_name='顺序')
    
    class Meta:
        verbose_name = '路线景点'
        verbose_name_plural = '路线景点管理'
        ordering = ['order']

class Review(models.Model):
    """景点评价"""
    id = models.AutoField(primary_key=True)
    spot = models.ForeignKey(TravelInfo, on_delete=models.CASCADE, verbose_name='景点')
    spot_name = models.CharField(max_length=255, verbose_name='景点名称', default='')
    user_id = models.IntegerField(verbose_name='用户ID', default=0)
    username = models.CharField(max_length=50, verbose_name='用户名', default='匿名用户')
    rating = models.IntegerField(verbose_name='评分', choices=[(1, '1分'), (2, '2分'), (3, '3分'), (4, '4分'), (5, '5分')])
    content = models.TextField(verbose_name='评价内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='评价时间')
    
    def save(self, *args, **kwargs):
        if self.spot and not self.spot_name:
            self.spot_name = self.spot.name
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.username} 对 {self.spot_name} 的评价'
    
    class Meta:
        verbose_name = '景点评价'
        verbose_name_plural = '景点评价管理'


class PageVisit(models.Model):
    """页面访问统计"""
    page_name = models.CharField(max_length=255, verbose_name='页面名称')
    page_url = models.CharField(max_length=500, verbose_name='页面URL')
    visit_count = models.IntegerField(default=0, verbose_name='访问次数')
    first_visit = models.DateTimeField(auto_now_add=True, verbose_name='首次访问时间')
    last_visit = models.DateTimeField(auto_now=True, verbose_name='最后访问时间')
    
    def __str__(self):
        return f'{self.page_name} - {self.visit_count}次'
    
    class Meta:
        verbose_name = '页面访问统计'
        verbose_name_plural = '页面访问统计管理'
        ordering = ['-visit_count']

class Recommendation(models.Model):
    """推荐结果"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='用户')
    spot = models.ForeignKey(TravelInfo, on_delete=models.CASCADE, verbose_name='景点')
    score = models.FloatField(verbose_name='推荐分数')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    def __str__(self):
        return f'{self.user.username if self.user else "未知用户"} - {self.spot.name} (分数: {self.score:.2f})'
    
    class Meta:
        verbose_name = '推荐结果'
        verbose_name_plural = '推荐结果管理'
        ordering = ['-score', '-created_at']

