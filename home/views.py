from collections import defaultdict

import numpy as np
from django.db.models import Q, Count, Avg, Case, When
from django.db.models.functions import TruncDate
from django.shortcuts import render
from django.http import JsonResponse
from home.models import TravelInfo, Review, Recommendation
from user.models import UserInfo
from utils import util
from datetime import datetime

def index(request):
    non_free_count = TravelInfo.objects.exclude(Q(actual_price='免费') | Q(actual_price__isnull=True)).count()
    pro_count = TravelInfo.objects.values('province').distinct().count()
    city_count = TravelInfo.objects.values('city').distinct().count()
    comment_count = TravelInfo.objects.values('review_count').distinct().count()
    # 获取热门景点数据
    hot_spots_sql = 'select name, value from city_hotspots order by value desc limit 10'
    hot_spots_res = util.query(hot_spots_sql)
    # 从TravelInfo表中获取景点的详细信息
    hot_spots = []
    for item in hot_spots_res:
        spot_name = item[0]
        spot_value = item[1]
        # 查询TravelInfo表获取详细信息
        try:
            travel_info = TravelInfo.objects.filter(name=spot_name).first()
            if travel_info:
                hot_spots.append({
                    'name': spot_name,
                    'value': spot_value,
                    'image_url': travel_info.image_url,
                    'location': f"{travel_info.city} - {travel_info.area}" if travel_info.city else "未知位置"
                })
            else:
                hot_spots.append({
                    'name': spot_name,
                    'value': spot_value,
                    'image_url': '',
                    'location': "未知位置"
                })
        except Exception as e:
            hot_spots.append({
                'name': spot_name,
                'value': spot_value,
                'image_url': '',
                'location': "未知位置"
            })
    
    # 获取销量前10的景点数据
    sales_spots_sql = 'select name, value from spot_sales order by value desc limit 10'
    sales_spots_res = util.query(sales_spots_sql)
    
    # 从TravelInfo表中获取景点的详细信息
    sales_spots = []
    for item in sales_spots_res:
        spot_name = item[0]
        spot_value = item[1]
        # 查询TravelInfo表获取详细信息
        try:
            travel_info = TravelInfo.objects.filter(name=spot_name).first()
            if travel_info:
                sales_spots.append({
                    'name': spot_name,
                    'value': spot_value,
                    'image_url': travel_info.image_url,
                    'price': travel_info.actual_price if travel_info.actual_price else "未知",
                    'city': travel_info.city if travel_info.city else "未知城市",
                    'tags': travel_info.tags if travel_info.tags else "无标签",
                    'rating': travel_info.rating if travel_info.rating else "0.0"
                })
            else:
                sales_spots.append({
                    'name': spot_name,
                    'value': spot_value,
                    'image_url': '',
                    'price': "未知",
                    'city': "未知城市",
                    'tags': "无标签",
                    'rating': "0.0"
                })
        except Exception as e:
            sales_spots.append({
                'name': spot_name,
                'value': spot_value,
                'image_url': '',
                'price': "未知",
                'city': "未知城市",
                'tags': "无标签",
                'rating': "0.0"
            })
    # 地图数据
    sql ='select name, value from city_stats'
    res= util.query(sql)
    
    # 创建默认省份列表，包含所有中国省份
    default_provinces = [
        '北京', '天津', '河北', '山西', '内蒙古', '辽宁', '吉林', '黑龙江',
        '上海', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南',
        '湖北', '湖南', '广东', '广西', '海南', '重庆', '四川', '贵州',
        '云南', '西藏', '陕西', '甘肃', '青海', '宁夏', '新疆','台湾'
    ]
    
    # 将查询结果转换为字典，便于查找
    province_dict = {}
    for item in res:
        province_dict[item[0]] = int(item[1])
    
    # 生成完整的地图数据，对于没有数据的省份，设置默认值0
    mapData = []
    for province in default_provinces:
        value = province_dict.get(province, 0)
        mapData.append({'name': province, 'value': value})
    content = {
        'non_free_count':non_free_count,
        'pro_count':pro_count,
        'city_count':city_count,
        'comment_count':comment_count,
        'mapData':mapData,
        'hot_spots': hot_spots,
        'sales_spots': sales_spots,
    }
    return render(request, 'index.html', content)

def travel_list(request):
    from django.core.paginator import Paginator

    # 获取搜索参数
    search_name = request.GET.get('search_name', '')
    selected_province = request.GET.get('province', '')
    
    # 构建查询
    queryset = TravelInfo.objects.all()
    
    # 按景点名称搜索
    if search_name:
        queryset = queryset.filter(name__icontains=search_name)
    
    # 按省份筛选
    if selected_province:
        queryset = queryset.filter(province=selected_province)
    
    # 获取所有省份列表（用于筛选下拉框）
    provinces = TravelInfo.objects.values_list('province', flat=True).distinct().order_by('province')
    
    # 基于用户评论的协同过滤推荐
    recommended_spots = get_collaborative_filtering_recommendations()
    
    # 将推荐结果融合到景点列表中
    if not search_name and not selected_province:
        # 没有查询条件时，使用推荐结果
        recommended_spot_names = list(recommended_spots)
        # 按推荐顺序排序景点
        recommended_ids = []
        for spot_name in recommended_spot_names:
            spot = TravelInfo.objects.filter(name=spot_name).first()
            if spot:
                recommended_ids.append(spot.id)
        
        # 如果有推荐结果，按推荐顺序排序
        if recommended_ids:
            # 使用Django的Case和When表达式实现自定义排序
            when_clauses = []
            for i, id in enumerate(recommended_ids):
                when_clauses.append(When(id=id, then=i))
            
            queryset = TravelInfo.objects.filter(id__in=recommended_ids).order_by(
                Case(*when_clauses, default=len(recommended_ids))
            )
    else:
        # 有查询条件时，从推荐结果中筛选符合条件的景点
        if recommended_spots:
            # 获取推荐景点的ID（保持推荐顺序）
            recommended_spot_ids = []
            for spot_name in recommended_spots:
                spot = TravelInfo.objects.filter(name=spot_name).first()
                if spot:
                    recommended_spot_ids.append(spot.id)
            
            # 筛选符合查询条件的推荐景点
            if recommended_spot_ids:
                # 先获取所有符合条件的推荐景点
                recommended_queryset = TravelInfo.objects.filter(
                    id__in=recommended_spot_ids
                )
                
                # 应用搜索条件
                if search_name:
                    recommended_queryset = recommended_queryset.filter(name__icontains=search_name)
                if selected_province:
                    recommended_queryset = recommended_queryset.filter(province=selected_province)
                
                # 如果有符合条件的推荐景点，优先显示并保持推荐顺序
                if recommended_queryset.exists():
                    # 获取符合条件的推荐景点ID列表（保持原推荐顺序）
                    filtered_recommended_ids = [id for id in recommended_spot_ids if id in recommended_queryset.values_list('id', flat=True)]
                    
                    # 按推荐顺序排序符合条件的推荐景点
                    if filtered_recommended_ids:
                        # 使用Django的Case和When表达式实现自定义排序
                        when_clauses = []
                        for i, id in enumerate(filtered_recommended_ids):
                            when_clauses.append(When(id=id, then=i))
                        
                        recommended_queryset = TravelInfo.objects.filter(id__in=filtered_recommended_ids).order_by(
                            Case(*when_clauses, default=len(filtered_recommended_ids))
                        )
                    
                    # 先显示推荐的景点，然后显示其他符合条件的景点
                    other_queryset = queryset.exclude(id__in=recommended_spot_ids)
                    # 确保两个查询集在合并之前都有排序
                    queryset = recommended_queryset.union(other_queryset.order_by('id'))
    
    # 分页
    paginator = Paginator(queryset, 10)  # 每页10条
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    content = {
        'page_obj': page_obj,
        'search_name': search_name,
        'selected_province': selected_province,
        'provinces': provinces,
        'recommended_spots': recommended_spots
    }

    return render(request, 'travel_list.html', content)

def get_collaborative_filtering_recommendations(user_id, top_n=10):
    """针对特定用户的协同过滤推荐算法"""
    # 获取所有评论数据
    reviews = Review.objects.all().values('user_id', 'spot_id', 'rating', 'spot__name')
    if not reviews:
        return set()
    # 构建用户-景点评分矩阵
    user_spot_ratings = defaultdict(dict)
    spot_users = defaultdict(set)
    for review in reviews:
        user_id_val = review['user_id']
        spot_id = review['spot_id']
        rating = review['rating']
        user_spot_ratings[user_id_val][spot_id] = rating
        spot_users[spot_id].add(user_id_val)
    # 检查目标用户是否有评分记录
    if user_id not in user_spot_ratings:
        return set()
    # 获取目标用户的历史评分
    target_user_ratings = user_spot_ratings[user_id]
    # 计算用户相似度（余弦相似度）
    def cosine_similarity(user1_ratings, user2_ratings):
        common_spots = set(user1_ratings.keys()) & set(user2_ratings.keys())
        if not common_spots:
            return 0.0
        ratings1 = np.array([user1_ratings[spot] for spot in common_spots])
        ratings2 = np.array([user2_ratings[spot] for spot in common_spots])
        norm1 = np.linalg.norm(ratings1)
        norm2 = np.linalg.norm(ratings2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return np.dot(ratings1, ratings2) / (norm1 * norm2)
    # 计算目标用户与其他所有用户的相似度
    similarities = []
    for other_user_id, other_ratings in user_spot_ratings.items():
        if user_id != other_user_id:
            sim = cosine_similarity(target_user_ratings, other_ratings)
            if sim > 0:
                similarities.append((other_user_id, sim))
    # 按相似度排序
    similarities.sort(key=lambda x: x[1], reverse=True)
    top_k_similar = similarities[:10]
    # 根据相似用户的评分计算推荐分数
    spot_scores = defaultdict(float)
    spot_rating_counts = defaultdict(int)
    for other_user_id, sim in top_k_similar:
        other_ratings = user_spot_ratings[other_user_id]
        for spot_id, rating in other_ratings.items():
            if spot_id not in target_user_ratings:  # 只推荐目标用户未评分过的景点
                spot_scores[spot_id] += sim * rating
                spot_rating_counts[spot_id] += 1
    # 计算平均推荐分数并排序
    final_scores = {}
    for spot_id in spot_scores:
        if spot_rating_counts[spot_id] > 0:
            final_scores[spot_id] = spot_scores[spot_id] / spot_rating_counts[spot_id]
    # 获取top_n个推荐景点
    sorted_spots = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
    # 返回推荐景点
    recommended_spots = []
    for i, (spot_id, score) in enumerate(sorted_spots, 1):
        spot = TravelInfo.objects.filter(id=spot_id).first()
        if spot:
            recommended_spots.append((spot.name, spot.province, score))
    return recommended_spots

def save_recommendations(user, recommendations, default_score=0.0):
    """
    保存推荐结果到数据库
    
    Args:
        user: User对象或None
        recommendations: 字典 {spot_id: score} 或集合 {spot_name}
        default_score: 默认推荐分数
    """
    try:
        # 清除旧的推荐结果
        if user:
            Recommendation.objects.filter(user=user).update(is_active=False)
        else:
            # 清除匿名用户的推荐
            Recommendation.objects.filter(user__isnull=True).update(is_active=False)

        if isinstance(recommendations, dict):
            # 推荐包含分数
            for spot_id, score in recommendations.items():
                spot = TravelInfo.objects.filter(id=spot_id).first()
                if spot:
                    Recommendation.objects.create(
                        user=user,
                        spot=spot,
                        score=score
                    )
        else:
            # 推荐只包含名称
            for spot_name in recommendations:
                spot = TravelInfo.objects.filter(name=spot_name).first()
                if spot:
                    Recommendation.objects.create(
                        user=user,
                        spot=spot,
                        score=default_score
                    )
    except Exception as e:
        # 如果数据库操作失败，记录错误但继续执行
        print(f"保存推荐结果失败: {e}")
# Create your views here.
def rating_stats(request):
    """评分分布统计"""
    from utils import util
    
    # 从rating_distribution数据库中获取数据
    sql = 'SELECT * FROM rating_distribution'
    res = util.query(sql)
    
    # 转换数据格式
    rating_data = []
    for item in res:
        rating_data.append({
            'value': item[2],  # 数量
            'name': f'{item[1]}分'  # 评分
        })
    
    content = {
        'rating_data': rating_data
    }
    
    return render(request, 'part1.html', content)

def hot_spots(request):
    """热门景点排行"""
    from utils import util
    import json
    
    # 从spot_sales数据库中获取数据（用于漏斗图）
    sql = 'SELECT * FROM spot_sales ORDER BY CAST(value AS UNSIGNED) DESC LIMIT 10'
    res = util.query(sql)
    
    # 转换数据格式（用于漏斗图）
    hot_data = []
    for item in res:
        hot_data.append({
            'value': int(item[2]),  # 评论数量
            'name': item[1]  # 景点名称
        })
    
    # 获取各城市热门景点数据（用于柱状图）
    city_sql = 'SELECT city, name, value FROM city_hotspots ORDER BY city, CAST(value AS DECIMAL(10,2)) DESC'
    city_res = util.query(city_sql)
    
    # 按城市分组
    city_hot_data = {}
    for item in city_res:
        city = item[0]
        name = item[1]
        value = float(item[2])
        
        if city not in city_hot_data:
            city_hot_data[city] = []
        
        # 每个城市最多取10个热门景点
        if len(city_hot_data[city]) < 10:
            city_hot_data[city].append({
                'name': name,
                'value': value
            })
    
    content = {
        'hot_data': hot_data,
        'city_hot_data': json.dumps(city_hot_data, ensure_ascii=False)
    }
    
    return render(request, 'part2.html', content)

def price_analysis(request):
    """景点门票价格分析"""
    price_data = []
    
    # 查询price_range表中的票价区间数据
    try:
        from utils import util
        sql = 'SELECT name, value FROM price_range ORDER BY id'
        results = util.query(sql)
        
        # 转换区间名称，使显示更友好
        range_mapping = {
            '0': '免费',
            '1-50': '1-50元',
            '50-100': '50-100元',
            '100-200': '100-200元',
            '200-500': '200-500元',
            '500-1000': '500-1000元',
            '1000+': '1000元以上'
        }
        
        for row in results:
            range_name = row[0]
            count = int(row[1])
            display_name = range_mapping.get(range_name, range_name)
            price_data.append({
                "range": display_name,
                "count": count
            })
    except Exception as e:
        # 如果获取数据失败，使用默认数据
        price_data = [
            {"range": "免费", "count": 0},
            {"range": "1-50元", "count": 0},
            {"range": "50-100元", "count": 0},
            {"range": "100-200元", "count": 0},
            {"range": "200-500元", "count": 0},
            {"range": "500-1000元", "count": 0},
            {"range": "1000元以上", "count": 0}
        ]
    
    content = {
        'price_data': price_data
    }
    
    return render(request, 'part3.html', content)

def word_cloud(request):
    """景点信息词云"""
    from utils import util
    
    # 从spot_wordcloud数据库中获取数据
    sql = 'SELECT name, value FROM spot_wordcloud'
    res = util.query(sql)
    
    # 转换数据格式
    wordcloud_data = []
    for item in res:
        wordcloud_data.append({
            'name': item[0],  # 关键词
            'value': int(item[1])  # 出现次数
        })
    
    content = {
        'wordcloud_data': wordcloud_data
    }
    
    return render(request, 'part4.html', content)

def region_spots_data(request):
    """从home_travelinfo提取区域和景点名称，保存到region_spots数据库"""
    from utils import util
    
    try:
        # 创建region_spots表（如果不存在）
        create_sql = '''
        CREATE TABLE IF NOT EXISTS region_spots (
            id INT AUTO_INCREMENT PRIMARY KEY,
            area VARCHAR(255),
            name VARCHAR(255) UNIQUE,
            INDEX idx_area (area)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        '''
        util.query(create_table_sql)
        
        # 从home_travelinfo提取区域和景点名称
        select_sql = 'SELECT area, name FROM home_travelinfo WHERE area IS NOT NULL AND area != "暂无" AND name IS NOT NULL'
        results = util.query(select_sql)
        
        # 保存到region_spots数据库，以景点名称为唯一标识
        insert_sql = 'INSERT IGNORE INTO region_spots (area, name) VALUES (%s, %s)'
        for row in results:
            area = row[0]
            name = row[1]
            if area and name:
                util.query(insert_sql, (area, name))
        
        return JsonResponse({'status': 'success', 'message': '数据已保存到region_spots数据库'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

def region_distribution(request):
    """景点区域分布"""
    region_data = []
    area_spots_data = []
    
    # 从region_distribution数据库中获取区域分布数据（用于左侧图表）
    try:
        from utils import util
        sql = 'SELECT name, value FROM region_distribution ORDER BY CAST(value AS UNSIGNED) DESC'
        results = util.query(sql)
        
        # 排除"暂无"数据，只取前30个区域
        for row in results:
            region_name = row[0]
            count = int(row[1])
            
            # 跳过"暂无"数据
            if region_name == '暂无':
                continue
            
            region_data.append({
                "name": region_name,
                "value": count
            })
            
            # 只取前30个区域
            if len(region_data) >= 30:
                break
    except Exception as e:
        # 如果获取数据失败，使用默认数据
        region_data = [
            {"name": "天安门/王府井地区", "value": 24},
            {"name": "陆家嘴", "value": 23},
            {"name": "星海广场/圣亚海洋世界/星海公园", "value": 20},
            {"name": "中山广场/人民路东港商务区", "value": 19},
            {"name": "西湖风景区/灵隐度假区", "value": 18},
            {"name": "海棠湾/三亚免税店/后海", "value": 17},
            {"name": "大雁塔/大唐不夜城", "value": 16},
            {"name": "沙坡头旅游景区", "value": 16}
        ]
    
    # 从part9数据库中获取区域-景点映射数据（用于右侧图表）
    try:
        from utils import util
        # 确保region_spots表存在并有数据
        util.query('CREATE TABLE IF NOT EXISTS part9 (id INT AUTO_INCREMENT PRIMARY KEY, area VARCHAR(255), name VARCHAR(255), UNIQUE KEY unique_name (name)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4')
        
        # 查询区域和景点数据
        spot_sql = 'SELECT area, name FROM region_spots WHERE area IS NOT NULL AND area != "暂无" ORDER BY area'
        spot_results = util.query(spot_sql)
        
        # 按区域分组
        area_spots_map = {}
        for row in spot_results:
            area = row[0]
            name = row[1]
            if area not in area_spots_map:
                area_spots_map[area] = []
            area_spots_map[area].append(name)
        
        # 转换为要求的格式
        for area, spots in area_spots_map.items():
            area_spots_data.append({
                "area": area,
                "name": spots  # 显示该区域所有景点
            })
    except Exception as e:
        # 如果获取数据失败，使用默认数据
        area_spots_data = [
            {"area": "龙王头沙滩/县城区", "name": ["龙王头沙滩", "平潭看日出", "平潭岛"]},
            {"area": "天安门/王府井地区", "name": ["天安门广场", "故宫博物院", "王府井步行街"]},
            {"area": "陆家嘴", "name": ["东方明珠", "上海环球金融中心", "金茂大厦"]}
        ]
    
    content = {
        'region_data': region_data,
        'area_spots_data': area_spots_data
    }
    
    return render(request, 'part5.html', content)

def ai_chat(request):
    """智能客服"""
    if request.method == 'POST':
        user_question = request.POST.get('question', '')
        
        # 从数据库中检索相关信息
        related_spots = TravelInfo.objects.filter(
            Q(name__icontains=user_question) |
            Q(city__icontains=user_question) |
            Q(province__icontains=user_question)
        )[:5]  # 只取前5个相关景点
        print(related_spots)
        
        # 构建上下文信息
        context = "以下是与用户问题相关的旅游景点信息：\n"
        for spot in related_spots:
            context += f"景点名称：{spot.name}\n"
            context += f"所在城市：{spot.city}\n"
            context += f"所在省份：{spot.province}\n"
            context += f"评分：{spot.rating}\n"
            context += f"票价：{spot.actual_price}\n"
            context += f"标签：{spot.tags}\n"
            context += f"与市中心距离：{spot.distance_from_center}\n"
            context += "\n"
        
        # 导入Get_Chat类
        import sys
        sys.path.append('AI')
        from AI.Get_Chat import Get_Chat
        
        try:
            # 创建Get_Chat实例
            chat = Get_Chat()
            
            # 构建完整问题，包含上下文信息
            full_question = f"{context}\n\n用户问题：{user_question}"
            
            # 调用AI获取回答
            answer = chat.get_chat_response(full_question)
            
            # 返回回答
            return JsonResponse({'success': True, 'answer': answer})
        except Exception as e:
            # 处理所有错误
            error_message = str(e)
            return JsonResponse({'success': False, 'answer': f"抱歉，我暂时无法回答您的问题。错误信息：{error_message}"})
    
    # GET请求返回页面
    return render(request, 'ai_chat.html')

def generate_travel_route(request):
    """生成旅游路线"""
    if request.method == 'POST':
        # 导入Get_Deepseek类
        import sys
        sys.path.append('AI')
        from AI.Get_Message import Get_Deepseek
        
        # 获取表单数据
        city = request.POST.get('city', '')
        season = request.POST.get('season', '')
        days = request.POST.get('days', '')
        budget = request.POST.get('budget', '')
        
        # 验证数据
        if not city or not season or not days or not budget:
            return JsonResponse({'success': False, 'message': '请填写所有必填字段'})
        
        try:
            # 创建Get_Deepseek实例
            deepseek = Get_Deepseek()
            
            # 调用AI生成旅游路线
            table_text = deepseek.get_ai_response(city, season, budget, days)
            
            # 解析表格为DataFrame
            df = deepseek.parse_table_to_dataframe(table_text)
            
            # 提取景点坐标信息
            points = []
            for _, row in df.iterrows():
                points.append({
                    'name': row['景点名称'],
                    'longitude': row['经度'],
                    'latitude': row['纬度']
                })
            
            # 构建响应数据
            route = {
                'city': city,
                'season': season,
                'days': days,
                'budget': budget,
                'table': table_text,
                'points': points
            }
            
            return JsonResponse({'success': True, 'route': route})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'生成旅游路线失败: {str(e)}'})
    
    # GET请求返回页面
    return render(request, 'travel_route.html')


def submit_review(request):
    """提交景点评价"""
    if request.method == 'POST':
        spot_id = request.POST.get('spot_id')
        rating = request.POST.get('rating')
        content = request.POST.get('content')
        
        try:
            # 获取景点
            spot = TravelInfo.objects.get(id=spot_id)
            
            # 获取用户信息
            user_id = request.session.get('user_id', 0)
            username = request.session.get('username', '匿名用户')
            
            # 如果用户已登录但session中没有username，从数据库获取
            if user_id != 0 and username == '匿名用户':
                try:
                    from user.models import UserInfo
                    user = UserInfo.objects.get(id=user_id)
                    username = user.username
                except:
                    pass
            
            # 创建评价
            review = Review.objects.create(
                spot=spot,
                user_id=user_id,
                username=username,
                rating=rating,
                content=content
            )
            
            # 更新景点的评分和评论数量
            reviews = Review.objects.filter(spot=spot)
            avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
            spot.rating = round(avg_rating, 1) if avg_rating else 0
            spot.review_count = reviews.count()
            spot.save()
            
            return JsonResponse({'success': True, 'message': '评价提交成功！'})
        except TravelInfo.DoesNotExist:
            return JsonResponse({'success': False, 'message': '景点不存在'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'提交失败：{str(e)}'})
    return JsonResponse({'success': False, 'message': '请使用POST请求'})

def user_stats(request):
    """后台管理 - 用户注册数统计页面"""
    user_stats_data = UserInfo.objects.annotate(date=TruncDate('created_at')).values('date').annotate(count=Count('id')).order_by('date')

    name_list = [str(items['date']) for items in user_stats_data]
    value_list = [items['count'] for items in user_stats_data]

    total_users = UserInfo.objects.count()
    today_users = UserInfo.objects.filter(created_at__date=datetime.now().date()).count()

    content = {
        'name_list': name_list,
        'value_list': value_list,
        'total_users': total_users,
        'today_users': today_users,
    }
    return render(request, 'user_stats.html', content)

