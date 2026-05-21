"""
创建少量用户并测试协同过滤算法
"""
import os
import django
import random
import time

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel.settings')
django.setup()

from user.models import UserInfo
from home.models import TravelInfo, Review
import numpy as np
from collections import defaultdict

def create_test_users():
    """创建测试用户"""
    print("=" * 60)
    print("创建测试用户")
    print("=" * 60)
    
    # 创建admin1用户（ID=1）
    admin1, created = UserInfo.objects.get_or_create(
        id=1,
        defaults={
            'username': 'admin1',
            'uemail': 'admin1@example.com',
            'uaddress': '',
            'uyoubian': '',
            'uphone': '',
            'avatar': ''
        }
    )
    if created:
        admin1.set_password('123456')
        admin1.save()
        print("创建用户: admin1 (ID: 1)")
    else:
        print("用户 admin1 (ID: 1) 已存在")
    
    # 创建其他9个测试用户
    for i in range(2, 11):
        username = f'test_user{i}'
        email = f'test_user{i}@example.com'
        
        user, created = UserInfo.objects.get_or_create(
            id=i,
            defaults={
                'username': username,
                'uemail': email,
                'uaddress': '',
                'uyoubian': '',
                'uphone': '',
                'avatar': ''
            }
        )
        
        if created:
            user.set_password('123456')
            user.save()
            print(f"创建用户: {username} (ID: {i})")
        else:
            print(f"用户 {username} (ID: {i}) 已存在")
    
    print("=" * 60)

def create_test_reviews():
    """为每个用户创建评论"""
    print("\n" + "=" * 60)
    print("为每个用户创建评论")
    print("=" * 60)
    
    # 获取所有用户
    users = UserInfo.objects.filter(id__lte=10)
    print(f"共有 {users.count()} 个用户需要创建评论")
    
    # 获取所有景点
    spots = list(TravelInfo.objects.all())
    print(f"共有 {len(spots)} 个景点可供评论")
    
    if not spots:
        print("没有景点数据，无法创建评论")
        return
    
    # 评论内容模板
    comments = [
        "景色迷人，拍照非常出片，强烈推荐！",
        "服务态度很好，环境整洁，体验不错！",
        "景点规模很大，玩了一整天，很开心！",
        "交通便利，设施齐全，是个好去处！",
        "门票价格合理，性价比高，推荐给大家！",
        "导游讲解很详细，学到了很多知识！",
        "人有点多，但风景真的很美，值得一去！",
        "整体体验很好，下次还会再来！",
        "建议早点去，避开人流高峰！",
        "这个景点非常棒，风景优美，值得推荐！"
    ]
    
    for user in users:
        # 为每个用户创建10条评论
        user_reviews = 0
        for _ in range(10):
            # 随机选择一个景点
            spot = random.choice(spots)
            
            # 随机评分 (1-5)
            rating = random.randint(1, 5)
            
            # 随机评论内容
            content = random.choice(comments)
            
            # 检查是否已经评论过
            existing_review = Review.objects.filter(user_id=user.id, spot=spot).first()
            if existing_review:
                continue
            
            # 创建评论
            review = Review(
                spot=spot,
                spot_name=spot.name,
                user_id=user.id,
                username=user.username,
                rating=rating,
                content=content
            )
            review.save()
            
            user_reviews += 1
            
            if user_reviews >= 10:
                break
        
        print(f"为用户 {user.username} 创建了 {user_reviews} 条评论")
    
    print("=" * 60)

def calculate_similarity():
    """计算用户之间的相似度"""
    print("\n" + "=" * 60)
    print("计算用户相似度")
    print("=" * 60)
    
    # 获取所有评论数据
    reviews = Review.objects.all().values('user_id', 'spot_id', 'rating')
    print(f"共有 {reviews.count()} 条评论数据")
    
    # 构建用户-景点评分矩阵
    user_spot_ratings = defaultdict(dict)
    for review in reviews:
        user_id = review['user_id']
        spot_id = review['spot_id']
        rating = review['rating']
        user_spot_ratings[user_id][spot_id] = rating
    
    print(f"共有 {len(user_spot_ratings)} 个用户参与评分")
    
    # 计算余弦相似度
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
    
    # 获取admin1的评分
    admin1_id = 1
    if admin1_id not in user_spot_ratings:
        print("admin1没有评分记录，无法计算相似度")
        return
    
    admin1_ratings = user_spot_ratings[admin1_id]
    print(f"admin1共评分 {len(admin1_ratings)} 个景点")
    
    # 计算admin1与其他用户的相似度
    similarities = []
    for user_id, user_ratings in user_spot_ratings.items():
        if user_id != admin1_id:
            user = UserInfo.objects.filter(id=user_id).first()
            username = user.username if user else f'user{user_id}'
            sim = cosine_similarity(admin1_ratings, user_ratings)
            similarities.append((user_id, username, sim))
    
    # 按相似度排序
    similarities.sort(key=lambda x: x[2], reverse=True)
    
    # 输出相似度列表
    print("\nadmin1与其他用户的相似度列表:")
    print("排名 | 用户ID | 用户名 | 相似度 | 共同评分景点数")
    print("-" * 60)
    
    for i, (user_id, username, sim) in enumerate(similarities, 1):
        user_ratings = user_spot_ratings[user_id]
        common_spots = set(admin1_ratings.keys()) & set(user_ratings.keys())
        print(f"{i:4d} | {user_id:6d} | {username:10s} | {sim:.4f} | {len(common_spots):12d}")
    
    print("=" * 60)

def main():
    print("开始执行测试任务...")
    
    # 1. 创建测试用户
    create_test_users()
    
    # 2. 创建测试评论
    create_test_reviews()
    
    # 3. 计算相似度
    calculate_similarity()
    
    print("\n测试任务完成！")

if __name__ == "__main__":
    main()
