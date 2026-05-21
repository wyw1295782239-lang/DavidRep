from utils import util

def check_province_images():
    # 查询每个省份的景点数量和有图片的景点数量
    sql = """
    SELECT province, 
           COUNT(*) as total_spots, 
           COUNT(image_url) as spots_with_images
    FROM travel_info 
    GROUP BY province 
    ORDER BY province
    """
    
    results = util.query(sql)
    
    print("省份图片情况统计:")
    print("-" * 60)
    print(f"{'省份':<10} {'总景点数':<10} {'有图片的景点数':<15} {'图片覆盖率':<10}")
    print("-" * 60)
    
    for row in results:
        province = row[0]
        total_spots = row[1]
        spots_with_images = row[2]
        
        if total_spots > 0:
            coverage = (spots_with_images / total_spots) * 100
            print(f"{province:<10} {total_spots:<10} {spots_with_images:<15} {coverage:.1f}%")
        else:
            print(f"{province:<10} {total_spots:<10} {spots_with_images:<15} {'N/A':<10}")
    
    print("-" * 60)
    
    # 查询没有图片的省份
    sql_no_images = """
    SELECT DISTINCT province 
    FROM travel_info 
    WHERE image_url IS NULL OR image_url = ''
    ORDER BY province
    """
    
    provinces_no_images = util.query(sql_no_images)
    
    print("\n没有图片的省份:")
    if provinces_no_images:
        for row in provinces_no_images:
            print(f"- {row[0]}")
    else:
        print("所有省份都有图片")

if __name__ == "__main__":
    check_province_images()
