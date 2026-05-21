"""
检查省份字段的实际值
"""
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel.settings')
django.setup()

from home.models import TravelInfo

# 获取所有不同的省份值
provinces = TravelInfo.objects.values_list('province', flat=True).distinct().order_by('province')

print('省份列表（前20个）:')
for i, province in enumerate(list(provinces)[:20], 1):
    print(f'{i}. {province}')

# 检查北京相关的景点
print('\n检查北京相关的景点:')
beijing_spots = TravelInfo.objects.filter(name__icontains='北京')
print(f'名称包含"北京"的景点数量: {beijing_spots.count()}')

if beijing_spots.exists():
    print('前5个名称包含"北京"的景点:')
    for i, spot in enumerate(beijing_spots[:5], 1):
        print(f'{i}. {spot.name} - 省份: {spot.province} - 城市: {spot.city}')
