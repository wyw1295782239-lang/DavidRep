import  pymysql
import sys
import os

# 将项目根目录添加到Python的搜索路径中
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
import pandas as pd
conn = pymysql.connect(
    host=Config.HOST,
    user=Config.USER,
    password=Config.PASSWORD,
    db=Config.DATABASE,
)
cursor = conn.cursor()
cursor.execute('SET FOREIGN_KEY_CHECKS = 0')
truncate_sql ='truncate table home_travelinfo'
cursor.execute(truncate_sql)
cursor.execute('SET FOREIGN_KEY_CHECKS = 1')
sql = 'insert into home_travelinfo(unique_id,area,name,review_count,rating,is_ad,is_recommended,city,'\
       'image_url,distance_from_center,tags,detail_link,market_price,discount_price,discount_description,'\
       'actual_price,price_type,price_type_description,is_free,longitude,latitude,popularity_score,province)'\
    ' values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
df=pd.read_csv('data_control.csv')

for index, row in df.iterrows():
    # 将 NaN 值转换为 None，以便 MySQL 能够处理
    row_data = tuple(None if pd.isna(value) else value for value in row)
    cursor.execute(sql, row_data)

conn.commit()
cursor.close()
conn.close()