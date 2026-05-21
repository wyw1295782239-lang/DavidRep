"""
数据库表重命名脚本
将Part1~Part9重命名为具有实际意义的表名
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel.settings')
django.setup()

from utils import util

# 定义表名映射关系
TABLE_MAPPING = {
    'Part1': 'rating_distribution',
    'Part2': 'spot_sales',
    'Part3': 'price_range',
    'Part4': 'region_distribution',
    'Part5': 'spot_wordcloud',
    'Part6': 'city_stats',
    'Part7': 'city_hotspots',
    'Part8': 'spot_rankings',
    'Part9': 'region_spots'
}

def rename_tables():
    """重命名所有表"""
    print("开始重命名数据库表...")
    print("=" * 50)

    for old_name, new_name in TABLE_MAPPING.items():
        try:
            # 检查旧表是否存在
            check_sql = f"SHOW TABLES LIKE '{old_name}'"
            result = util.query(check_sql)

            if result:
                # 重命名表
                rename_sql = f"RENAME TABLE {old_name} TO {new_name}"
                util.query(rename_sql)
                print(f"[OK] {old_name} -> {new_name}")
            else:
                print(f"[SKIP] {old_name} table does not exist")

        except Exception as e:
            print(f"[FAIL] Rename {old_name} failed: {e}")

    print("=" * 50)
    print("Table rename completed!")

def verify_tables():
    """验证重命名后的表"""
    print("\nVerifying renamed tables...")
    print("=" * 50)

    for old_name, new_name in TABLE_MAPPING.items():
        try:
            check_sql = f"SHOW TABLES LIKE '{new_name}'"
            result = util.query(check_sql)

            if result:
                print(f"[OK] {new_name} exists")
            else:
                print(f"[FAIL] {new_name} does not exist")

        except Exception as e:
            print(f"[FAIL] Check {new_name} failed: {e}")

    print("=" * 50)

if __name__ == "__main__":
    rename_tables()
    verify_tables()