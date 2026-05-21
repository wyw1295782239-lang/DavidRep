import pandas as pd
df = pd.read_csv(
    'data.csv',names =['唯一标识','所在区域','景点名称','评论数量','评分','是否为广告内容',
                       '是否被推荐','城市名称','图片','到市中心距离','标签','详情页链接','市场票价','优惠价格','优惠描述','实际票价','价格类型','价格类型描述','是否免费',
                       '经度','纬度','热度评分','省份'])
df = df.drop_duplicates(subset=['唯一标识'])
df['评分'] = df['评分'].fillna(0)#将评分列进行空值填充
df['标签'] =df['标签'].str.replace('[','').str.replace(']','').str.replace("'",'')
df['热度评分'] = df['热度评分'].fillna(0)
df['评论数量'] =df['评论数量'].fillna(0)

df=df.replace('[]','')
df=df.fillna('暂无')
df.to_csv('data_control.csv',index=False)

