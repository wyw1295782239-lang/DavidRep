"""
查看Review表的spot_id来源
"""
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel.settings')
django.setup()

from home.models import Review, TravelInfo

def check_spot_id_source():
    """查看spot_id的来源"""
    print("=" * 60)
    print("查看Review表的spot_id字段来源")
    print("=" * 60)
    
    # 查看所有评论及其对应的景点信息
    reviews = Review.objects.all()
    print(f"\n共有 {reviews.count()} 条评论\n")
    
    print("评论详情:")
    for i, review in enumerate(reviews[:10], 1):
        print(f"\n{i}. 评论信息:")
        print(f"   - 评论ID: {review.id}")
        print(f"   - spot_id: {review.spot_id}")
        print(f"   - spot_name: {review.spot_name}")
        print(f"   - 用户: {review.username} (user_id: {review.user_id})")
        print(f"   - 评分: {review.rating}分")
        print(f"   - 评论内容: {review.content[:30]}...")
        
        # 显示关联的景点信息
        if review.spot:
            print(f"   关联的景点信息:")
            print(f"   - 景点ID: {review.spot.id}")
            print(f"   - 景点名称: {review.spot.name}")
            print(f"   - 景点省份: {review.spot.province}")
            print(f"   - 景点城市: {review.spot.city}")
    
    print("\n" + "=" * 60)
    print("spot_id字段来源说明:")
    print("=" * 60)
    print("""
spot_id字段是一个外键（FOREIGN KEY），指向home_travelinfo表。

在Review模型的定义中：
    spot = models.ForeignKey(TravelInfo, on_delete=models.CASCADE, verbose_name='景点')

这意味着：
1. spot_id存储的是TravelInfo表的主键（id）
2. 通过spot_id，Review表与TravelInfo表建立了关联关系
3. 当创建评论时，spot_id会自动从TravelInfo表中选择一个有效的景点ID

数据来源：
- 在创建评论时，系统会从TravelInfo表中选择一个景点
- 将该景点的id作为spot_id存储到Review表中
- 例如：选择"安吉竹博园"景点（id=某个值），将其id存储到spot_id字段
""")

if __name__ == "__main__":
    check_spot_id_source()
