try:
    import jieba
    JIEBA_AVAILABLE = True
except Exception as e:
    JIEBA_AVAILABLE = False
    pass
import pandas as pd
import pymysql
import os
import sys

# 将项目根目录添加到Python的搜索路径中
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from collections import Counter

# 获取当前文件所在目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))

# 延迟加载数据，避免模块导入时立即读取CSV
def get_dataframe():
    """延迟加载data_control.csv数据"""
    global df
    if 'df' not in globals():
        df = pd.read_csv(os.path.join(current_dir, 'data_control.csv'))
    return df

# 创建数据库连接的函数
def get_conn():
    conn=pymysql.connect(
            host=Config.HOST,
            user=Config.USER,
            password=Config.PASSWORD,
            database=Config.DATABASE,
            port=Config.PORT,
            autocommit=True)
    cursor = conn.cursor()
    return cursor, conn


#评分分布
def part1():
    cursor,conn=get_conn()
    data = df.copy()
    # print(data)  # 注释掉可能导致编码问题的print
    data =data[data['评分']!=0.0]
    score_counts=data['评分'].value_counts()
    # 清空表
    truncate_sql = 'truncate table rating_distribution'
    cursor.execute(truncate_sql)
    conn.commit()
    sql = 'insert into rating_distribution(score,value) values(%s,%s)'
    for index, row in  score_counts.items():
        cursor.execute(sql,(index,row))
    conn.commit()
    cursor.close()
    conn.close()
#创建评分表
def part2():
    cursor,conn=get_conn()
    top_10 = df.nlargest(10,"评论数量")[['景点名称','评论数量']]
    # print(top_10)  # 注释掉可能导致编码问题的print
    #清空表
    truncate_sql = 'truncate table spot_sales'
    cursor.execute(truncate_sql)
    conn.commit()

    sql = 'insert into spot_sales(name,value) values(%s,%s)'
    #将分析结果写入表
    for index, row in top_10.iterrows():
        cursor.execute(sql,(row['景点名称'],row['评论数量']))
    conn.commit()
    cursor.close()
    conn.close()
#票价区间分离
def part3():
    cursor,conn=get_conn()
    df['实际票价'] = df['实际票价'].astype(str)
    df['实际票价'] = df['实际票价'].replace('免费',0)
    df['实际票价'] = df['实际票价'].replace('[]','不详')

    #将类型转化为float
    # 先将'不详'替换为0，然后再转换为float
    df['实际票价'] = df['实际票价'].replace('不详',0)
    df['实际票价'] = df['实际票价'].astype(float)

    #单独统计票价为0的数量
    count_free = (df['实际票价'] == 0).sum()

    #定义价格区间
    bins = [0,1,50,100,200,500,1000,float('inf')]
    labels=['0','1-50','50-100','100-200','200-500','500-1000','1000+']
    price_dis = pd.cut(df['实际票价'],bins=bins,labels=labels,right=False)
    print_counts=price_dis.value_counts().sort_index()
    print(print_counts)
#写入数据、
#清空表
    truncate_sql='truncate table price_range'
    cursor.execute(truncate_sql)
    conn.commit()
    sql = 'insert into price_range(name,value) values(%s,%s)' \
 \
    #将分析结果写入表
    for index, row in print_counts.items():
        cursor.execute(sql,(index,row))
    conn.commit()
    cursor.close()
    conn.close()
#区域分布
def part4():
    cursor, conn = get_conn()
    data=df.copy()
    area_counts=data['所在区域'].value_counts()
    print(area_counts)

    # 清空表
    truncate_sql = 'truncate table region_distribution'
    cursor.execute(truncate_sql)
    conn.commit()

    sql = 'insert into region_distribution(name,value) values(%s,%s)' \
 \
        # 将分析结果写入表
    for index, row in area_counts.items():
        cursor.execute(sql, (index, row))
    conn.commit()
    cursor.close()
    conn.close()
def load_stopwords():
    lines=[]
    with open('stop_words.txt', 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line:  # 文件末尾
                break
            line = line.rstrip('\n')
            lines.append(line)
    return lines


#停用词
def part5():
    if not JIEBA_AVAILABLE:
        print("跳过part5: jieba库未安装")
        return
        
    cursor, conn = get_conn()
    all_texts =df['标签'].fillna('').tolist()+df['景点名称'].fillna('').tolist()
    # print(all_texts)  # 注释掉可能导致编码问题的print
    #加载停用词
    stopwords = load_stopwords()
    # print(stopwords)  # 注释掉可能导致编码问题的print
    words=[]
    for text in all_texts:
        seq_list=jieba.cut(text)
        #过滤停用词
        words.extend([word for word in seq_list if word not in stopwords and word.strip()!=''])
    word_count = Counter(words)

    word_count =pd.DataFrame(word_count.items(),columns=['word','count'])
    # print(word_count)  # 注释掉可能导致编码问题的print
    # 清空表
    truncate_sql = 'truncate table spot_wordcloud'
    cursor.execute(truncate_sql)
    conn.commit()

    sql = 'insert into spot_wordcloud(name,value) values(%s,%s)'
    # 将分析结果写入表
    for index, row in word_count.iterrows():
        cursor.execute(sql, (row['word'],row['count']))
    conn.commit()
    # 关闭数据库连接
    cursor.close()
    conn.close()
#各省份城市排行
def part6():
    # 创建数据库连接
    cursor, conn = get_conn()
    data= df.copy()
    province_num = data['省份'].value_counts()
    print(province_num)
     #清空表
    truncate_sql = 'truncate table city_stats'
    cursor.execute(truncate_sql)
    sql = 'insert into city_stats(name,value) values(%s,%s)'
    for index, row in province_num.items():
        cursor.execute(sql, (index, row))
    
    # 关闭数据库连接
    cursor.close()
    conn.close()
#各地区热门景点排行
def part7():
    # 创建数据库连接
    cursor, conn = get_conn()
    data= df.sort_values('热度评分',ascending=False).groupby('城市名称').head(10)
    print(data)
    rank = data[['城市名称','景点名称','热度评分']]
    print(rank)
    truncate_sql = 'truncate table city_hotspots'
    cursor.execute(truncate_sql)
    sql = 'insert into city_hotspots(city,name,value) values(%s,%s,%s)'
    for index, row in  rank.iterrows():
        cursor.execute(sql, (row['城市名称'],row['景点名称'], row['热度评分']))
    
    # 关闭数据库连接
    cursor.close()
    conn.close()
#各省份景点平均分
def part8():
    # 创建数据库连接
    cursor, conn = get_conn()
    data=df.copy()
    data=data[data['评分']!=0.0]
    data['评分']=data['评分'].astype(float)
    pro_rating=data.groupby('省份')['评分'].agg(['count','mean']).reset_index()
    print(pro_rating)
    truncate_sql = 'truncate table spot_rankings'
    cursor.execute(truncate_sql)
    sql = 'insert into spot_rankings(name,count,value) values(%s,%s,%s)'
    for index, row in pro_rating.iterrows():
        cursor.execute(sql, (row['省份'],row['count'], row['mean']))
    # 关闭数据库连接
    cursor.close()
    conn.close()

def part9():
    """从home_travelinfo提取区域和景点名称，保存到region_spots数据库"""
    import pymysql
    
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='123456',
        database='travel',
        charset='utf8mb4'
    )
    cursor = conn.cursor()
    
    try:
        # 创建region_spots表（如果不存在）
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS region_spots (
            id INT AUTO_INCREMENT PRIMARY KEY,
            area VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            UNIQUE KEY unique_name (name)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        '''
        cursor.execute(create_table_sql)
        
        # 从home_travelinfo提取区域和景点名称
        select_sql = 'SELECT area, name FROM home_travelinfo WHERE area IS NOT NULL AND area != "暂无" AND name IS NOT NULL'
        cursor.execute(select_sql)
        results = cursor.fetchall()
        
        # 保存到part9数据库，以景点名称为唯一标识
        insert_sql = 'INSERT IGNORE INTO part9 (area, name) VALUES (%s, %s)'
        for row in results:
            area = row[0]
            name = row[1]
            if area and name:
                cursor.execute(insert_sql, (area, name))
        
        conn.commit()
        print('part9数据已保存')
    except Exception as e:
        print(f'Error: {e}')
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':

    part1()
    part2()
    part3()
    part4()
    part5()
    part6()
    part7()
    part8()